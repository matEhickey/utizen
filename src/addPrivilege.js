/* global process */


const fs = require('fs-extra')
const xml2js = require('xml2js')
var parseString = xml2js.parseStringPromise

const AddNetworkPrivilege = async function (appName, privilege) {
    const filename = `/tmp/utizen/${appName}/config.xml`
    console.warn(appName)
    console.warn(filename)
    
    
    var content = fs.readFileSync(filename, 'utf8')

    const { res } = await parseString(content).then(res => ({ res })).catch(error => ({ error }))

    var newPrivilege = { '$': { name: privilege } };
    res["widget"]["tizen:privilege"].push(newPrivilege);
    
    var builder = new xml2js.Builder();
    var xml = builder.buildObject(res);
    
    fs.writeFileSync(filename, xml); 
}

if(process.argv.length < 4) {
  console.error("usage: node addPrivilege.js <filename> <privilege>")
  process.exit()
}

const appName = process.argv[2]
const privilege = process.argv[3]

AddNetworkPrivilege(appName, privilege)