# OpenThread Stack — SDK Fork Patches

This directory contains Silicon Labs' forks of the upstream OpenThread repositories (under `util/third_party/`), along with patch files that make the changes Silicon Labs has made relative to upstream visible and reproducible.

## Files

| File                | Description                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| `openthread.patch`  | Full diff of Silicon Labs' `openthread` fork against its upstream ancestor commit.  |
| `ot-br-posix.patch` | Full diff of Silicon Labs' `ot-br-posix` fork against its upstream ancestor commit. |
| `upstream-commits`  | Records the upstream ancestor commits this release's forks diverge from.            |
| `CHANGELOG.md`      | Per-release summary of fork changes relative to upstream.                           |

## Fork changes by release

See [CHANGELOG.md](CHANGELOG.md) for a summary of what Silicon Labs has changed in each SDK release. The `.patch` files remain the authoritative, complete diff for a given release.

## Inspecting the patches

Open the `.patch` files directly in any text editor or diff viewer to see what Silicon Labs has added or modified relative to upstream.

## Applying patches to a clean upstream clone

The `upstream-commits` file is the authoritative reference for the ancestor commit of each fork. To reproduce the exact Silicon Labs fork state from a clean upstream checkout:

```bash
# For openthread
git clone https://github.com/openthread/openthread.git
cd openthread
git checkout <openthread ancestor commit from upstream-commits>
git apply /path/to/openthread_stack/openthread.patch

# For ot-br-posix
git clone https://github.com/openthread/ot-br-posix.git
cd ot-br-posix
git checkout <ot-br-posix ancestor commit from upstream-commits>
git apply /path/to/openthread_stack/ot-br-posix.patch
```

> **Note:** If you make additional changes on top of these patches, or start from a different upstream ancestor commit than those listed in `upstream-commits`, the following may be required to maintain a working integration with the Silicon Labs SDK:
>
> - Updates to component metadata files (`.slcc`)
> - Updates to platform code
> - Updates to OpenThread configuration
>
> Contact [Silicon Labs Support](https://www.silabs.com/support) for assistance. Silicon Labs cannot guarantee the performance or behavior of non-standard forks that have not been tested for a given release.
