const crypto = require("crypto");

function hash_base64(password) {
  return crypto.createHash("sha256").update(password).digest("base64");
}

console.log(hash_base64("myVerySecurePassword").toString());
