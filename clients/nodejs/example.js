const { diagnose } = require("./client");

function api(path, query) {
  const publicKey = process.env.DIAGNOSE_PUBLIC_KEY || "<YOUR PUBLIC KEY>";
  const secretKey = process.env.DIAGNOSE_SECRET_KEY || `<YOUR SECRET KEY>`;
  return diagnose({ publicKey, secretKey }, path, query);
}

async function main() {
  const result = await api("/v1/prognose", {
    source: "Battery01",
  });
  console.log(result);
}

main().catch((e) => console.error(e));
