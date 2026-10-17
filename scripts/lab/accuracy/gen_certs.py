"""Generate the lab's TLS material into ./certs (run with any Python that has
`cryptography`, e.g. the probe's virtualenv). Throwaway keys, lab use only."""
import datetime as dt
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

OUT = Path(__file__).resolve().parent / "certs"
NOW = dt.datetime.now(dt.timezone.utc)


def make(name, bits, not_before, not_after, digest):
    key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, f"{name}.lab.invalid")])
    cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(subject)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(not_before).not_valid_after(not_after)
            .add_extension(x509.SubjectAlternativeName(
                [x509.DNSName(f"{name}.lab.invalid")]), critical=False)
            .sign(key, digest))
    (OUT / f"{name}.key").write_bytes(key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()))
    (OUT / f"{name}.crt").write_bytes(cert.public_bytes(serialization.Encoding.PEM))


OUT.mkdir(exist_ok=True)
make("weak", 1024, NOW - dt.timedelta(days=800), NOW - dt.timedelta(days=30), hashes.SHA256())
make("strong", 2048, NOW - dt.timedelta(days=1), NOW + dt.timedelta(days=365), hashes.SHA256())
for p in OUT.iterdir():
    p.chmod(0o644)           # read by the container's non-root python
print(f"wrote {sorted(p.name for p in OUT.iterdir())}")
