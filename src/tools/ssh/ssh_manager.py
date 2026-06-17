import paramiko
import logging
import io

logger = logging.getLogger(__name__)

def ssh_run_command(host: str, username: str, command: str, port: int = 22, password: str = None, key_content: str = None) -> str:
    """Run a shell command on a remote server via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if key_content:
            key_file = io.StringIO(key_content.strip())
            # Try RSA key first, fallback to Ed25519/ECDSA
            try:
                pkey = paramiko.RSAKey.from_private_key(key_file)
            except Exception:
                key_file.seek(0)
                try:
                    pkey = paramiko.Ed25519Key.from_private_key(key_file)
                except Exception:
                    key_file.seek(0)
                    pkey = paramiko.ECDSAKey.from_private_key(key_file)
            client.connect(hostname=host, port=port, username=username, pkey=pkey, timeout=15)
        elif password:
            client.connect(hostname=host, port=port, username=username, password=password, timeout=15)
        else:
            return "Error: Either password or key_content must be provided for SSH authentication."
            
        stdin, stdout, stderr = client.exec_command(command, timeout=30)
        
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        exit_status = stdout.channel.recv_exit_status()
        
        client.close()
        
        if exit_status != 0:
            return f"SSH Command Failed (exit code {exit_status}):\nStdout: {out}\nStderr: {err}"
        return out if out else "Command executed successfully with no output."
        
    except Exception as e:
        return f"SSH Connection/Execution Error: {str(e)}"
