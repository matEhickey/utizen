/* global process */

const fs = require('fs-extra')
const xml2js = require('xml2js')
var parseString = xml2js.parseStringPromise

const AllowNavigation = async function (appName) {
    const filename = `/tmp/utizen/${appName}/config.xml`

    var content = fs.readFileSync(filename, 'utf8')

    const { res } = await parseString(content).then(res => ({ res })).catch(error => ({ error }))

    var newProperty = "*";
    res["widget"]["tizen:allow-navigation"] = newProperty;

    var builder = new xml2js.Builder();
    var xml = builder.buildObject(res);
    fs.writeFileSync(filename, xml);
}

if(process.argv.length < 3) {
  console.error("usage: node addPrivilege.js <appname>")
  process.exit()
}

const appName = process.argv[2]

AllowNavigation(appName)