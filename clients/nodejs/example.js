const { diagnose } = require("./client");

async function main() {
  process.env.DIAGNOSE_PUBLIC_KEY = "<YOUR PUBLIC KEY>";
  process.env.DIAGNOSE_SECRET_KEY = `<YOUR SECRET>`;
  const result = await diagnose("/v1/prognose", { source: "Battery01" });
  console.log(result);
}

main().catch((e) => console.error(e));
