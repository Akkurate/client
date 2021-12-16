const crypto = require("crypto");
const url = require("url");
const zlib = require("zlib");

// generate nonce minimal length 70
function generateNonce() {
  return new Date().getTime() + crypto.randomBytes(32).toString("hex");
}

// handle content gracefully
// if a server supports gzip, it will be decompressed
async function handleGzip(response, body) {
  return new Promise((resolve, reject) => {
    if (response.headers["content-encoding"] == "gzip") {
      zlib.gunzip(body, function (err, dezipped) {
        if (err) return reject(err);
        return resolve(dezipped.toString());
      });
    } else {
      return resolve(body);
    }
  });
}

// collect response in chunks
async function getContent(response) {
  return new Promise((resolve, reject) => {
    let body = "";
    response.on("data", (chunk) => (body += chunk));
    response.on("end", () => resolve(handleGzip(response, body)));
    response.on("error", (err) => reject(err));
  });
}

function getFetchOptions() {
  if (process.env.LOCAL_DIAGNOSE_CLIENT) {
    return {
      http: require("http"),
      options: {
        protocol: "http",
        hostname: "localhost",
        port: 5555,
      },
    };
  } else {
    return {
      http: require("https"),
      options: {
        protocol: "https",
        hostname: "publicapi.diagnose.fi",
        port: 443,
      },
    };
  }
}

// main function
async function diagnose(keys, targetURL, query) {
  const fetchOptions = getFetchOptions();
  const urlOptions = {
    ...fetchOptions.options,
    pathname: targetURL,
    query: query,
  };
  const requestUrl = url.parse(url.format(urlOptions));
  const Nonce = generateNonce();

  const PublicKey = keys.publicKey;
  const SecretKey = keys.secretKey;

  const Signature = crypto
    .createHmac("sha512", SecretKey)
    .update(Nonce)
    .digest("hex");

  const options = {
    hostname: requestUrl.hostname,
    port: requestUrl.port,
    path: requestUrl.path,
    rejectUnauthorized: true,
    method: "GET",
    headers: {
      PublicKey,
      Nonce,
      Signature,
    },
  };

  return new Promise((resolve, reject) => {
    const req = fetchOptions.http.request(options, async (res) => {
      const body = await getContent(res);
      if (res.statusCode !== 200) {
        return reject({ code: res.statusCode, message: body.trim() });
      }
      // we assume the content is json
      try {
        resolve(JSON.parse(body));
      } catch (e) {
        reject(e);
      }
    });
    req.on("error", function (err) {
      return reject(err);
    });
    req.end();
  });
}

module.exports = { diagnose };
