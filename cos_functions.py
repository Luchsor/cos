#run certreq.exe -new -q machine request.inf request.req

import subprocess
import tempfile

import textwrap

from dataclasses import dataclass


temp_dir = tempfile.mkdtemp()

@dataclass
class policy_variables:
    subject: str
    friendly_name: str
    alternative_names: list[str]

def get_policy(variables: policy_variables) -> str:
    alternative_names_lines = [f'_continue_ = "dns={name}"' for name in variables.alternative_names]
    alternative_names_str = '\n'.join(alternative_names_lines)

    return textwrap.dedent(f"""[Version]
    
Signature="$Windows NT$"

[NewRequest]
Subject = "{variables.subject}"
FriendlyName = "{variables.friendly_name}"

Exportable = TRUE
HashAlgorithm = SHA256
KeyLength = 2048
KeySpec = 1
KeyUsage = 0xA0
MachineKeySet = TRUE
PrivateKeyArchive = FALSE
ProviderName = "Microsoft RSA SChannel Cryptographic Provider"
ProviderType = 12
RequestType = PKCS10
SMIME = FALSE
UseExistingKeySet = FALSE

[EnhancedKeyUsageExtension]
OID=1.3.6.1.5.5.7.3.1 ; Server Authentication
OID=1.3.6.1.5.5.7.3.2 ; Client Authentication

[Extensions]
; Subject Alternative Name (SANs)
2.5.29.17 = \"{{text}}\"
{alternative_names_str}
    """).strip()



def run_cmd(cmd: str):
    try:
        print(f"> Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"> Command:")
        print(f">> RC: {e.returncode}")
        print(f">> STDOUT: {e.stdout.decode()}")
        print(f">> STDERR: {e.stderr.decode()}")
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.stdout, e.stderr)

def create_request(policy_variables: policy_variables):
    with tempfile.NamedTemporaryFile(suffix='.inf', delete=False) as inf_file, tempfile.NamedTemporaryFile(suffix='.req', delete=True) as req_file:
        print(f"> Creating request...")
        print(f">> INF File: {inf_file.name}")
        print(f">> REQ File: {req_file.name}")

        content = get_policy(policy_variables)
        # Write the content to the inf file
        inf_file.write(content.encode())

        
        
        run_cmd(f'certreq.exe -new -q -machine "{inf_file.name}" "{req_file.name}"')