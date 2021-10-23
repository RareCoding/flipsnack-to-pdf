const fs = require('fs');
const path = require('path');
const re = "/page_[0-9]*/original";

let rawdata = fs.readFileSync(path.resolve(__dirname, 'www.flipsnack.com.json'));
let network = JSON.parse(rawdata);
let pages = [...Array(35)];
let a = 0;
Object.entries(network.log.entries).forEach(
    ([key, value]) => {
        if (value.request.url!==undefined && value.request.url!==null) {
            if (value.request.url.match(re)){
                let page_url = value.request.url;
                pages[parseInt(page_url.split('/')[7].split('_')[1])]=page_url;
                a++;
            }
        }
    }
);
console.log(a);
console.log(pages);

const http = require('https'); // or 'https' for https:// URLs
// const file = fs.createWriteStream(__dirname+"/pages/"+"page_001.jpeg");
//     const request = http.get(pages[1], function(response) {
//       response.pipe(file);
//     });
let counter = -1;
for (let u of pages) {
    if (u ==  undefined) { 
        console.error(counter++);
        continue; 
    }

    const file = fs.createWriteStream(__dirname+"/pages/"+"page_"+String(counter++)+".jpeg");
    const request = http.get(u, function(response) {
      response.pipe(file);
    });
}
