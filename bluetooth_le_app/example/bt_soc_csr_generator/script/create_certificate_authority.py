#!/usr/bin/env python3

# Copyright 2026 Silicon Laboratories Inc. www.silabs.com
#
# SPDX-License-Identifier: Zlib
#
# The licensor of this software is Silicon Laboratories Inc.
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

'''Certificate Authority generator

Create an EC key pair and a certificate for either the Central or an Intermediate Authority of the given level.

Prerequisites:
Python 3.9 or higher.
Python packages contained in `requirements.txt`.
  Run `pip install -r requirements.txt` to install all requirements for the application.
For intermediate CA creation, the higher level (n-1) CA must be present. (Except for root CA generation.)
'''
# Metadata
__author__ = 'Silicon Laboratories, Inc'
__copyright__ = 'Copyright 2026, Silicon Laboratories, Inc.'

import os
import stat
import datetime
import argparse
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from jinja2 import FileSystemLoader, Environment
from pathlib import Path
from production_line_tool import generate_serial_number, add_certificate_to_database

WORKING_DIR = Path.home() / ".silabs" / "certificates"
TEMPLATE_FILE = Path(__file__).parent / 'sl_bt_cbap_root_cert.h.jinja'

def main(level,
         validity,
         subj_country,
         subj_state,
         subj_locality,
         subj_organization,
         subj_organizational_unit,
         subj_common_name,
         subj_email_address,
         subj_policy_oid):

    # Check arguments
    if level < 0:
        raise Exception('Authority level must be greater than or equal to zero!')
    if validity < 1:
        raise Exception('Valid period must be greater than or equal to one day!')

    # Paths
    if level == 0:
        name = 'central'
    else:
        name = 'intermediate_' + str(level)

    path_dir = (WORKING_DIR / (name + '_authority')).resolve()

    # Check if certificate authority already exists
    if path_dir.is_dir():
        raise FileExistsError(f'Directory: {path_dir} already exists. Please remove it first.')
    print(f"Output directory: {path_dir}")
    path_dir.mkdir(parents=True, exist_ok=True)

    path_key = path_dir / 'private_key.pem'
    path_cert = path_dir / 'certificate.pem'
    path_template = TEMPLATE_FILE

    if level == 0:
        path_database = path_dir / 'issued_certificates.yaml'
    else:
        # For intermediate certificate creation, check the existence of the higher certificate.
        if level == 1:
            prev_name = 'central'
        else:
            prev_name = 'intermediate_' + str(level - 1)

        path_prev_dir = (WORKING_DIR / (prev_name + '_authority')).resolve()
        print(f"Issuer Certificate Authority: {path_prev_dir}")
        path_prev_key = path_prev_dir / 'private_key.pem'
        path_prev_cert = path_prev_dir / 'certificate.pem'
        path_database = path_prev_dir / 'issued_certificates.yaml'

        if not path_prev_key.is_file() or not path_prev_cert.is_file() or not path_database.is_file():
            raise FileNotFoundError(f'{prev_name} authority cannot be found at {path_prev_dir}')

    # Generate EC key pair. Use X9.62/SECG curve over a 256 bit prime field (aka prime256v1).
    key = ec.generate_private_key(ec.SECP256R1())

    # Write private key to file in PEM format.
    with open(path_key, 'wb') as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Change file permissions
    os.chmod(path_key, stat.S_IREAD + stat.S_IWRITE)
    print(name + ' authority EC private key created.')

    # Pack certificate subjects
    subjects = x509.Name([
        x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, subj_country),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, subj_organization),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME, subj_organizational_unit),
        x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, subj_state),
        x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, subj_common_name),
        x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, subj_locality),
        x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, subj_email_address),
    ])

    if level == 0:
        # Create root certificate. Self-signing.
        cert = create_certificate(key.public_key(),
                                  subjects,
                                  validity,
                                  subj_policy_oid,
                                  key,
                                  subjects,
                                  path_database)
    else:
        # Create intermediate certificate.
        # Retrieve the private key and the certificate of the higher authority.
        with open(path_prev_key, 'rb') as f:
            root_key = serialization.load_pem_private_key(f.read(), password=None)

        with open(path_prev_cert, 'rb') as f:
            root_cert = x509.load_pem_x509_certificate(f.read())

        # Check the validity of the higher authority.
        # Note: if there is a revocation list, it should be also checked if the certificate is revoked or not.
        now = datetime.datetime.now(datetime.timezone.utc)
        if now < root_cert.not_valid_before_utc or root_cert.not_valid_after_utc < now:
            raise Exception(f'The validity period of {path_prev_cert} has expired.')

        # Sign with the key of the higher authority.
        cert = create_certificate(key.public_key(),
                                  subjects,
                                  validity,
                                  subj_policy_oid,
                                  root_key,
                                  root_cert.subject,
                                  path_database)

    # Write the certificate to file in PEM format.
    with open(path_cert, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    convert_header(path_cert, path_template) # Create header for SoC example
    print(f'{name} authority certificate created under: {path_dir}')

def create_certificate(public_key, subjects, validity, policy_oid, signing_key, issuer, path_database):
    ''' Create an x509 certificate object.

    Keyword arguments:
    public_key -- The public key of the certificate.
    subjects -- x509 certificate subjects.
    validity -- Validity period in days starting from the moment of creation.
    policy_oid -- Certificate policy
    signing_key -- The key to be used to sign the certificate with.
    issuer -- The issuer of the certificate.
    path_database -- Path to the database file.
    Return values:
    cert -- The created certificate.
    '''
    # Create certificate
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder()
        .subject_name(subjects)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(generate_serial_number(path_database))
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=validity)))

    # Add extensions
    cert = cert.add_extension(x509.SubjectKeyIdentifier.from_public_key(public_key), critical=False)
    cert = cert.add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)

    # Add certificate policy if present
    if policy_oid is not None:
        obj_id = x509.ObjectIdentifier(policy_oid)
        policy_info = [x509.PolicyInformation(obj_id, [])]
        cert = cert.add_extension(x509.CertificatePolicies(policies=policy_info), critical=True)

    # Sign certificate
    cert = cert.sign(signing_key, hashes.SHA256())
    add_certificate_to_database(cert, path_database)
    return cert

def convert_header(path_pem, path_template):
    '''Create a header file out of a PEM certificate that can be used
    directly by the Gecko SDK SoC sample applications.

    Keyword arguments:
    path_pem -- Path to the certificate file in PEM format.
    path_template -- Path to the jinja2 template.
    Return values:
    path_header -- Path to the certificate header file.
    '''
    path_pem = Path(path_pem)
    path_template = Path(path_template)

    # Check input
    if not path_pem.exists():
        raise FileNotFoundError('Cannot find certificate file.')

    # Load certificate
    with path_pem.open('r') as f:
        crt = f.readlines()

    # Remove PEM certificate delimiters
    crt.pop(0)
    crt.pop()

    # Format string
    i = 0
    while i < len(crt):
        if i < len(crt) - 1:
            crt[i] = '  "' + crt[i].strip() + '" \\\n'
        else:
            crt[i] = '  "' + crt[i].strip() + '"'
        i = i + 1

    crt = ''.join(crt)

    # Load jinja template
    env = Environment()
    env.loader = FileSystemLoader(path_template.parent)

    # Write to file
    path_header = path_pem.parent / path_template.stem

    with path_header.open('w') as f:
        f.write(env.get_template(path_template.name).render(sl_bt_cbap_root_cert=crt))

    print(str(path_header) + ' created.')
    return path_header

def load_args():
    '''Parse command line arguments'''
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-l', '--level',
                        default='0',
                        type=int,
                        help='Authority level. If zero passed, root certificate '\
                             'will be created. With greater values than zero, '\
                             'intermediate certificate will be created with '\
                             'the given level.')

    parser.add_argument('-v', '--validity',
                        default='365',
                        type=int,
                        help='The valid period of the certificate in days starting '\
                             'from the moment of generation.')

    parser.add_argument('--country',
                        default='US',
                        type=str.upper,
                        help='The country subject of the x509 certificate.')

    parser.add_argument('--state',
                        default='Texas',
                        help='The state subject of the x509 certificate.')

    parser.add_argument('--locality',
                        default='Austin',
                        help='The locality subject of the x509 certificate.')

    parser.add_argument('--organization',
                        default='Silicon Laboratories',
                        help='The organization subject of the x509 certificate.')

    parser.add_argument('--organizationalUnit',
                        default='Wireless',
                        help='The organizational unit subject of the x509 certificate.',
                        dest='organizational_unit')

    parser.add_argument('--commonName',
                        default='Silabs',
                        help='The common name unit subject of the x509 certificate.',
                        dest='common_name')

    parser.add_argument('--emailAddress',
                        default='support@silabs.com',
                        help='The e-mail address unit subject of the x509 certificate.',
                        dest='email_address')

    parser.add_argument('-c', '--certificatePolicy',
                        help='The optional Certificate Policy Information extension. '\
                             'Only a policy OID is supported.',
                        dest='policy_oid')

    return parser.parse_args()

if __name__ == '__main__':
    args = load_args()

    main(args.level,
         args.validity,
         args.country,
         args.state,
         args.locality,
         args.organization,
         args.organizational_unit,
         args.common_name,
         args.email_address,
         args.policy_oid)
