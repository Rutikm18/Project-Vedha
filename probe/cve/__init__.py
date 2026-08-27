"""
cve — vulnerability (CVE) correlation layer.

SEPARATE from the probe's collection scanners. The probe emits facts (service /
product / version / CPE) and NEVER a CVE claim; this package owns the offline
vulnerability database (NVD + KEV + EPSS) and maps facts -> prioritized CVE
findings. It is the "manager-side" correlation the probe architecture defers to.
"""
