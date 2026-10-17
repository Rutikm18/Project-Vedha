/** Browser-safe IP literal parsing. URL's IPv6 parser performs no network I/O. */
export function parseScanIp(raw: unknown): { host: string; bits: number; value: bigint } | null {
  if (typeof raw !== "string") return null;
  const text = raw.trim();
  if (!text || /[\s,;\[\]%-]/.test(text)) return null;
  const parts = text.split("/");
  if (parts.length > 2) return null;
  const [address, prefix] = parts;
  if (!address.includes(":")) {
    const octets = address.split(".");
    if (octets.length !== 4 || octets.some(x => !/^(0|[1-9]\d{0,2})$/.test(x) || Number(x) > 255)
      || (prefix !== undefined && prefix !== "32")) return null;
    return { host: address, bits: 32, value: octets.reduce((n, x) => (n << BigInt(8)) + BigInt(x), BigInt(0)) };
  }
  if (prefix !== undefined && prefix !== "128") return null;
  try {
    const host = new URL(`http://[${address}]/`).hostname.slice(1, -1);
    const halves = host.split("::");
    const left = halves[0] ? halves[0].split(":") : [];
    const right = halves.length === 2 && halves[1] ? halves[1].split(":") : [];
    const groups = halves.length === 2 ? [...left, ...Array(8 - left.length - right.length).fill("0"), ...right] : left;
    if (groups.length !== 8) return null;
    return { host, bits: 128, value: groups.reduce((n, x) => (n << BigInt(16)) + BigInt(`0x${x}`), BigInt(0)) };
  } catch { return null; }
}

export function scanIpInCidr(raw: string, cidr: string): boolean {
  const ip = parseScanIp(raw);
  const [address, prefix, extra] = cidr.trim().split("/");
  const network = parseScanIp(address);
  if (!ip || !network || extra !== undefined || network.bits !== ip.bits) return false;
  if (prefix !== undefined && !/^(0|[1-9]\d{0,2})$/.test(prefix)) return false;
  const bits = prefix === undefined ? ip.bits : Number(prefix);
  if (bits < 0 || bits > ip.bits) return false;
  const shift = BigInt(ip.bits - bits);
  return ip.value >> shift === network.value >> shift;
}

export function scanIpAllowed(raw: string, scope: string[], excluded: string[] = []): boolean {
  return scope.some(cidr => scanIpInCidr(raw, cidr)) && !excluded.some(cidr => scanIpInCidr(raw, cidr));
}

export interface ScanAssetOption { ip_address: string; hostname?: string | null }

export function deepScanAssetOptions(assets: ScanAssetOption[], scope: string[], excluded: string[] = []): ScanAssetOption[] {
  const seen = new Set<string>();
  return assets.filter(asset => {
    const ip = parseScanIp(asset?.ip_address);
    if (!ip || !scanIpAllowed(ip.host, scope, excluded) || seen.has(ip.host)) return false;
    seen.add(ip.host);
    return true;
  });
}
