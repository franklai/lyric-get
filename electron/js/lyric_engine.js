if (require) {
    var fetch = require('node-fetch');
    var he = require('he');
    var striptags = require('striptags');
}

class LyricFactory {
    static makeParser(url) {
        if (url.indexOf('kasi-time.com') !== -1) {
            return new KasiTime(url);
        } else {
            return null;
        }
    }
}

class LyricBase {
    constructor(url) {
        this.url = url;
    }

    get(url) {
        if (url) {
            this.url = url;
        }

        return new Promise( (resolve, reject) => {
            this.parse_page()
            .then( () => {
                const full_lyric = this.get_full();

                resolve(full_lyric);
            });
        });
    }

    parse_page() {
        console.log('Please implement parse_page function!');
        return true;
    }

    get_full() {
        let template = [];

        if (this.title) {
            template.push(this.title);
            template.push('');
        }

        if (this.artist) {
            template.push(`歌手：${this.artist}`);
        }
        if (this.lyricist) {
            template.push(`作詞：${this.lyricist}`);
        }
        if (this.composer) {
            template.push(`作曲：${this.composer}`);
        }
        if (this.arranger) {
            template.push(`編曲：${this.arranger}`);
        }

        if (template.length > 2) {
            template.push('');
            template.push('');
        }
        template.push(this.lyric);

        return template.join('\n');
    }

    get_html(url) {
        return new Promise( (resolve, reject) => {
            fetch(url)
            .then( (response) => resolve(response.text()) )
            .catch( () => reject() );
        });
    }

    find_string_by_prefix_suffix(text, prefix, suffix, including=true) {
        let start = text.indexOf(prefix);

        if (start === -1) {
            return null;
        }

        let end = text.indexOf(suffix, start);
        if (end === -1) {
            return null;
        }

        if (including) {
            return text.substring(start, end + suffix.length);
        } else {
            return text.substring(start + prefix.length, end);
        }
    }

    get_first_group_by_pattern(input, pattern) {
        let matches = input.match(pattern);
        if (matches) {
            return matches[1];
        }
        return null;
    }
}

class KasiTime extends LyricBase {
    parse_page() {
        const url = this.url;

        return new Promise( (resolve, reject) => {
            this.get_html(url)
            .then( (html) => {
                if (!html) {
                    reject();
                    return;
                }

                if (!this.find_lyric(html)) {
                    console.error(`Failed to get lyric of url [${url}]`);
                    reject();
                    return false;
                }

                if (!this.find_song_info(html)) {
                    console.info(`Failed to get song info of url: ${url}`);
                }
                
                resolve();
                return true;
            });
        });
    }

    find_song_info(html) {
        let ret = true;

        let pattern = '<h1>(.*?)</h1>';
        let value = this.get_first_group_by_pattern(html, pattern);
        if (value) {
            this.title = value.trim();
        } else {
            console.log('!Failed to get title');
            ret = false;
        }

        const prefix = '<div class="person_list">';
        const suffix = '</div>';
        let info_table = this.find_string_by_prefix_suffix(html, prefix, suffix, false);

        const patterns = {
            'artist': '歌手',
            'lyricist': '作詞',
            'composer': '作曲',
            'arranger': '編曲'
        };

        for (let key of Object.keys(patterns)) {
            const pattern = patterns[key];

            const prefix = `<th>${pattern}</th>`;
            const suffix = '</td>';

            let value = this.find_string_by_prefix_suffix(info_table, prefix, suffix, false);
            if (!value) {
                console.log(`Failed to get info of ${key}`);
                continue;
            }

            value = value.replace(/[\t\n]/g, '');
            value = striptags(value);
            value = he.decode(value);
            value = value.trim();
            if (value) {
                this[key] = value;
            }
        }

        return ret;
    }

    find_lyric(html) {
        const prefix = "var lyrics = '";
        const suffix = "';";

        let lyric = this.find_string_by_prefix_suffix(html, prefix, suffix, false);
        lyric = lyric.replace(/<br>/g, '\n');
        lyric = he.decode(lyric);
        lyric = lyric.trim();

        this.lyric = lyric;

        return true;
    }
}


if (require.main === module) {
    const url = 'http://www.kasi-time.com/item-78895.html';

    const obj = new KasiTime(url);

    obj.get(url)
    .then((full) => {
        if (!full) {
            console.log(`Failed to get lyric of ${url}`);
            return;
        }

        console.log(url);
        console.log('===== begin =====');
        console.log(full);
        console.log('===== end =====');
    });

}
