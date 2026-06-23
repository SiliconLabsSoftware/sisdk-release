/*
 * @Copyright 2023 Secure-IC S.A.S.
 * This file relies on Secure-IC S.A.S. software and patent portfolio.
 * This file cannot be used nor duplicated without prior approval from Secure-IC S.A.S.
 */

#include "../include/sxsymcrypt/aead.h"
#include "../include/sxsymcrypt/keyref.h"
#include "../include/sxsymcrypt/statuscodes.h"
#include "keyrefdefs.h"
#include "aeaddefs.h"
#include "blkcipherdefs.h"
#include "crypmasterregs.h"
#include "hw.h"
#include "cmdma.h"
#include "cmaes.h"

#define SX_CHACHAPOLY_NONCE_SZ 12u
#define SX_CHACHAPOLY_COUNTER_SIZE 4u
#define SX_CHACHAPOLY_KEY_SZ 32u
#define SX_CHACHAPOLY_TAG_SIZE 16u
#define SX_CHACHAPOLY_CTX_GRANULARITY_SZ 64u
#define SX_CHACHAPOLY_BLOCK_SZ 64u

/** Size of ChaCha20Poly1305 context saving state, in bytes
 * The ChaCha20Poly1305 context saving state is made of ChaCha20 state(first 16
 * bytes) and Poly1305(next 32 bytes). */
#define CHACHAPOLY_CTX_STATE_SZ (16 + 32)

#define CHACHA20_CTX_STATE_SZ (16)

/** Mode Register value for context loading */
#define CHACHAPOLY_MODEID_CTX_LOAD (1u << 5)
/** Mode Register value for context saving */
#define CHACHAPOLY_MODEID_CTX_SAVE (1u << 6)


static const char zeros[SX_CHACHAPOLY_TAG_SIZE] = {0};

static int lenAlenC_chachapoly(size_t aadsz, size_t datasz, uint8_t *out);

static void set_nonce_chachapoly(struct sxaead *c);


static const struct sx_aead_cmdma_tags ba417aeadtags = {
    .cfg = DMATAG_BA417 | DMATAG_CONFIG(0x00),
    .key = DMATAG_BA417 | DMATAG_CONFIG(0x04),
    .iv_or_state = DMATAG_BA417 | DMATAG_CONFIG(0x28),
    .nonce = DMATAG_BA417 | DMATAG_CONFIG(0x2C),
    .aad = DMATAG_BA417 | DMATAG_DATATYPE_HEADER,
    .tag = DMATAG_BA417,
    .data = DMATAG_BA417,
};


static const struct sx_aead_cmdma_cfg ba417chachapolycfg = {
    .decr = CM_CFG_DECRYPT << 2,
    .mode = AEAD_MODEID_CHACHAPOLY,
    .dmatags = &ba417aeadtags,
    .verifier = zeros,
    .lenAlenC = lenAlenC_chachapoly,
    .set_nonce = set_nonce_chachapoly,
    .ctxsave = CHACHAPOLY_MODEID_CTX_SAVE,
    .ctxload = CHACHAPOLY_MODEID_CTX_LOAD,
    .granularity = SX_CHACHAPOLY_CTX_GRANULARITY_SZ,
    .statesz = CHACHAPOLY_CTX_STATE_SZ,
    .inputminsz = 0,
    .tagminsz = 1,
    .hwtagverif = 1
};


static const struct sx_blkcipher_cmdma_tags ba417blkciphertags = {
    .cfg = DMATAG_BA417 | DMATAG_CONFIG(0x00),
    .key = DMATAG_BA417 | DMATAG_CONFIG(0x04),
    .iv_or_state = DMATAG_BA417 | DMATAG_CONFIG(0x28),
    .data = DMATAG_BA417,
};


static const struct sx_blkcipher_cmdma_cfg ba417chacha20cfg = {
    .decr = CM_CFG_DECRYPT << 2,
    .ctxsave = CHACHAPOLY_MODEID_CTX_SAVE,
    .ctxload = CHACHAPOLY_MODEID_CTX_LOAD,
    .dmatags = &ba417blkciphertags,
    .statesz = CHACHA20_CTX_STATE_SZ,
    .mode = 0x01,
    .inminsz = 1,
    .granularity = 1,
    .blocksz = SX_CHACHAPOLY_BLOCK_SZ,
};


static void sx_memcpy(void* dst, const void* src, size_t length)
{
    for (size_t i = 0; i < length; i++)
        ((uint8_t*) dst)[i] = ((uint8_t*) src)[i];
}


static void set_nonce_chachapoly(struct sxaead *c)
{
    /* In AEAD context, for BA417, the counter that must be provided and
    * initialized with 1. counter size is 4 bytes. Starting at position 16
    * due to lenAlenC that uses first 16 bytes of extramem */
    c->extramem[16] = 0;
    c->extramem[17] = 0;
    c->extramem[18] = 0;
    c->extramem[19] = 1;

    ADD_INDESC_PRIV(c->dma, OFFSET_EXTRAMEM(c) + 16, SX_CHACHAPOLY_COUNTER_SIZE,
        c->cfg->dmatags->iv_or_state);

    ADD_INDESC_PRIV(c->dma,
        (OFFSET_EXTRAMEM(c) + sizeof(c->extramem) - c->cfg->statesz),
        SX_CHACHAPOLY_NONCE_SZ, c->cfg->dmatags->nonce);
}


static int sx_blkcipher_create_chacha20_ba417(struct sxblkcipher *c,
    const struct sxkeyref *key, const uint32_t counter, const char *nonce,
    const uint32_t dir)
{
    SX_COMPATIBILTY_STORAGE unsigned int compatibleba417 = ~0u;

    if (KEYREF_IS_INVALID(key))
        return SX_ERR_INVALID_KEYREF;
    if (KEYREF_IS_USR(key))
        if (key->sz != SX_CHACHAPOLY_KEY_SZ)
            return SX_ERR_INVALID_KEY_SZ;

    if (compatibleba417 == ~0u)
        compatibleba417 = sx_cmdma_list_compatible(REG_HW_PRESENT_BA417);

    c->dma.regs = sx_cmdma_find_available(compatibleba417);
    c->cfg = &ba417chacha20cfg;

    if (!compatibleba417)
        return SX_ERR_INCOMPATIBLE_HW;

    if (!c->dma.regs)
        return SX_ERR_RETRY;

    sx_cmdma_newcmd(&c->dma, c->descs, sizeof(c->descs),
        c->cfg->mode | dir | KEYREF_CHACHAPOLY_HWKEY_CONF(key->cfg),
        c->cfg->dmatags->cfg);
    if (KEYREF_IS_USR(key))
        ADD_CFGDESC(c->dma, key->key, SX_CHACHAPOLY_KEY_SZ, c->cfg->dmatags->key);

    /* For BA417, initialization vector(16 bytes) is a concatenation of
     * counter(first 4 bytes) and the nonce(last 12 bytes). */
    c->extramem[3] = (char)((counter >> 0) & 0xFF);
    c->extramem[2] = (char)((counter >> 8) & 0xFF);
    c->extramem[1] = (char)((counter >> 16) & 0xFF);
    c->extramem[0] = (char)((counter >> 24) & 0xFF);
    sx_memcpy(&c->extramem[SX_CHACHAPOLY_COUNTER_SIZE], nonce, SX_CHACHAPOLY_NONCE_SZ);
    ADD_INDESC_PRIV(c->dma, OFFSET_EXTRAMEM(c),
            SX_CHACHAPOLY_COUNTER_SIZE + SX_CHACHAPOLY_NONCE_SZ,
            c->cfg->dmatags->iv_or_state);

    c->key = key;
    c->compatible = compatibleba417;
    c->textsz = 0;
    c->is_multifeed = 0;
    c->extradatasz = 0;

    return SX_OK;
}


int sx_blkcipher_create_chacha20_enc(struct sxblkcipher *c,
    const struct sxkeyref *key, const uint32_t counter, const char *nonce)
{
    return sx_blkcipher_create_chacha20_ba417(c, key, counter, nonce,
            CM_CFG_ENCRYPT);
}


int sx_blkcipher_create_chacha20_dec(struct sxblkcipher *c,
    const struct sxkeyref *key, const uint32_t counter, const char *nonce)
{
    return sx_blkcipher_create_chacha20_ba417(c, key, counter, nonce,
            ba417chacha20cfg.decr);
}


static int lenAlenC_chachapoly(size_t aadsz, size_t datasz, uint8_t *out)
{
    uint32_t i = 0;
    for (i = 0; i < 8; i++) {
        out[i] = aadsz & 0xFF;
        aadsz >>= 8;
    }
    out += 8;
    for (i = 0; i < 8; i++) {
        out[i] = datasz & 0xFF;
        datasz >>= 8;
    }

    return 1;
}


static int sx_aead_create_chacha20poly1305(struct sxaead *c,
    const struct sxkeyref *key, const char *nonce, const uint32_t dir)
{
    SX_COMPATIBILTY_STORAGE unsigned int compatibleba417 = ~0u;

    if (KEYREF_IS_INVALID(key))
        return SX_ERR_INVALID_KEYREF;
    if (KEYREF_IS_USR(key))
        if (key->sz != SX_CHACHAPOLY_KEY_SZ)
            return SX_ERR_INVALID_KEY_SZ;

    if (compatibleba417 == ~0u) {
        compatibleba417 = sx_cmdma_list_compatible(REG_HW_PRESENT_BA417);
    }
    c->dma.regs = sx_cmdma_find_available(compatibleba417);
    c->cfg = &ba417chachapolycfg;

    if (!compatibleba417)
        return SX_ERR_INCOMPATIBLE_HW;

    if (!c->dma.regs)
        return SX_ERR_RETRY;

    sx_cmdma_newcmd(&c->dma, c->descs, sizeof(c->descs),
        c->cfg->mode | dir | KEYREF_CHACHAPOLY_HWKEY_CONF(key->cfg),
        c->cfg->dmatags->cfg);
    if (KEYREF_IS_USR(key))
        ADD_CFGDESC(c->dma, key->key, SX_CHACHAPOLY_KEY_SZ, c->cfg->dmatags->key);

    /* In AEAD context, for BA417, the counter that must be provided and
     * initialized with 1. counter size is 4 bytes. Starting at position 16
     * due to lenAlenC that uses first 16 bytes of extramem */
    c->extramem[16] = 0;
    c->extramem[17] = 0;
    c->extramem[18] = 0;
    c->extramem[19] = 1;

    ADD_INDESC_PRIV(c->dma, OFFSET_EXTRAMEM(c) + 16, SX_CHACHAPOLY_COUNTER_SIZE,
            c->cfg->dmatags->iv_or_state);
    ADD_CFGDESC(c->dma, nonce, SX_CHACHAPOLY_NONCE_SZ, c->cfg->dmatags->nonce);

    /* Backup the nonce in case we won't call HW when context saving */
    sx_memcpy(c->extramem + sizeof(c->extramem) - c->cfg->statesz, (char *)nonce, SX_CHACHAPOLY_NONCE_SZ);

    c->tagsz = SX_CHACHAPOLY_TAG_SIZE;
    c->expectedtag = c->cfg->verifier;
    c->discardaadsz = 0;
    c->totalaadsz = 0;
    c->datainsz = 0;
    c->dataintotalsz = 0;
    c->extraaadsz = 0;
    c->extraaadptr = c->extraaadmem;
    c->no_exec = 0;
    c->key = key;
    c->compatible = compatibleba417;

    return SX_OK;
}


int sx_aead_create_chacha20poly1305_enc(struct sxaead *c,
    const struct sxkeyref *key, const char *nonce)
{
    return sx_aead_create_chacha20poly1305(c, key, nonce, 0);
}


int sx_aead_create_chacha20poly1305_dec(struct sxaead *c,
    const struct sxkeyref *key, const char *nonce)
{
    return sx_aead_create_chacha20poly1305(c, key, nonce,
            ba417chachapolycfg.decr);
}
