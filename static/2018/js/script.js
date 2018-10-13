/* eslint func-names: 0, no-var: 0, vars-on-top:0, prefer-template: 0, prefer-arrow-callback:0 */
(function () {
  if (!document.querySelectorAll) {
    return;
  }

  var links = document.querySelectorAll('.pure-menu-link');
  links = Array.prototype.slice.call(links);

  var $ = function (id) {
    return document.getElementById(id);
  };
  var q = function (selector) {
    return document.querySelector(selector);
  };

  var formQuery = $('query_form');
  var inputUrl = $('url');
  var btnSubmit = $('submit_btn');
  var divLoading = $('loading_div');
  var divLyric = $('lyric_div');
  var textareaLyric = $('lyric_textarea');

  var showContent = function (id) {
    var activeCls = 'content-active';
    q('.' + activeCls).classList.remove(activeCls);
    $(id).classList.add(activeCls);

    var selectedCls = 'pure-menu-selected';
    q('.' + selectedCls).classList.remove(selectedCls);
    q('.pure-menu-item[data-content-id=' + id + ']').classList.add(selectedCls);
  };
  var updateTextareaHeight = function () {
    textareaLyric.style.height = '100px';
    var height = textareaLyric.scrollHeight;
    textareaLyric.style.height = height + 20 + 'px';
  };

  var setErrorMsg = function (msg) {
    if (msg === false) {
      divLoading.style.display = 'none';
      divLyric.style.display = 'block';
      return;
    }

    divLoading.innerHTML = msg;
    divLoading.style.display = 'block';
    divLyric.style.display = 'none';
  };
  var setLoading = function () {
    setErrorMsg('Loading...');
    btnSubmit.disabled = true;
  };
  var setError = function () {
    var errMsg = '<span style="color: red;">Failed to get lyric. Please contact franklai.</span>';
    setErrorMsg(errMsg);
    btnSubmit.disabled = false;
  };
  var setResult = function (lyric) {
    if (!lyric) {
      setError();
      return;
    }

    setErrorMsg(false);
    btnSubmit.disabled = false;

    textareaLyric.value = lyric;
    updateTextareaHeight(lyric);
  };


  links.forEach(function (link) {
    link.addEventListener('click', function (evt) {
      evt.preventDefault();

      var pn = evt.target.parentNode;
      if (!pn || !pn.dataset) {
        return;
      }

      var id = pn.dataset.contentId;
      showContent(id);
    });
  });

  var selectLyric = function () {
    textareaLyric.select();
  };
  $('select').addEventListener('click', function () {
    selectLyric();
  });
  if (
    document.queryCommandSupported &&
    document.queryCommandSupported('copy')
  ) {
    var msg = q('.copied-msg');

    $('copy').addEventListener('click', function () {
      selectLyric();
      document.execCommand('copy');

      msg.classList.add('fadeout');
    });

    msg.addEventListener('transitionend', function () {
      msg.classList.remove('fadeout');
    });
  } else {
    $('copy').disabled = true;
  }
  inputUrl.addEventListener('click', function () {
    inputUrl.select();
  });

  var doAjaxQuery = function (val) {
    var url = '/app?url=' + encodeURIComponent(val);

    fetch(url)
      .then(function (resp) {
        resp
          .json()
          .then(function (json) {
            if (!json || !json.lyric) {
              setError();
              return;
            }
            setResult(json.lyric);
          })
          .catch(function () {
            setError();
          });
      })
      .catch(function () {
        setError();
      });
  };
  var doElectronQuery = function (val) {
    try {
      const engine = require('lyric-get-engine'); // eslint-disable-line global-require
      engine
        .get_full(val)
        .then(function (lyric) {
          if (!lyric) {
            setError();
            return;
          }

          setResult(lyric);
        })
        .catch(function (reason) {
          setError();
          console.log('Error:', reason);
        });
    } catch (err) {
      console.log('Error:', err);
    }
  };

  var doQuery = function () {
    var val = inputUrl.value.trim();
    if (val === '' || val.toLowerCase().match('https?://') === null) {
      return false;
    }

    setLoading();

    if (
      window.process &&
      window.process.versions &&
      window.process.versions.electron !== undefined
    ) {
      return doElectronQuery(val);
    }

    return doAjaxQuery(val);
  };

  $('examples').addEventListener('click', function (evt) {
    if (evt.target.tagName.toLowerCase() !== 'a') {
      return;
    }
    if (evt.metaKey || evt.ctrlKey || evt.shiftKey || evt.altKey) {
      return;
    }
    evt.preventDefault();

    inputUrl.value = evt.target.href;

    showContent('main');
    doQuery();
  });

  formQuery.addEventListener('submit', function (evt) {
    evt.preventDefault();
    doQuery();
  });
}());
