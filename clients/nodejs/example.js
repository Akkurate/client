const { createClient } = require("./client");

const publicKey = process.env.DIAGNOSE_PUBLIC_KEY || "<YOUR PUBLIC KEY>";
const secretKey = process.env.DIAGNOSE_SECRET_KEY || `<YOUR SECRET KEY>`;

async function main() {
  const client = createClient(publicKey, secretKey);
  const result = await client.get("/v1/prognose", {
    source: "Battery01",
  });
  console.log(JSON.stringify(result, null, 2));
}

main().catch((e) => console.error(e));
