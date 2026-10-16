/** Download a two-scan comparison (?format=csv|json) — BFF proxy that keeps the
 *  backend's content-type and content-disposition so the browser saves the file. */
import { forward } from "../../../../../lib/operator-proxy";

export async function GET(req: Request) {
  return forward(req, "/findings/compare/export");
}
