      // var config = {
        // mode: "pac_script",
        // pacScript: {
          // data: "function FindProxyForURL(url, host) {\n" +
                // "  if (shExpMatch(url, \"http://www3.kanpani.jp/amf?_c=*\"))\n" +
                // "    return 'PROXY localhost:8899';\n" +
                // "  return 'DIRECT';\n" +
                // "}"
      // }};
      // chrome.proxy.settings.set(
          // {value: config, scope: 'regular'},
          // function() {});
      var config = {
        mode: "pac_script",
        pacScript: {
        //http://img3.kanpani.jp/img/quest/chapter_select/main/004_on.png
        //http://img3.kanpani.jp/img/quest/chapter_title/11.png
          data: "function FindProxyForURL(url, host) {\n" +
                "  if (shExpMatch(url, \"http://www*.kanpani.jp/amf?_c=Quest.special_enter&_u=*\") || shExpMatch(url, \"http://www*.kanpani.jp/amf?_c=Quest.main_enter&_u=*\") || shExpMatch(url, \"http://www*.kanpani.jp/amf?_c=Quest.next&_u=*\") || shExpMatch(url, \"http://www*.kanpani.jp/amf?_c=Quest.main_stages&_u=*\"))\n" +
                "    return 'PROXY localhost:8899';\n" +
                "  if (shExpMatch(url, \"http://img*.kanpani.jp/img/quest/chapter_select/main/*\") || shExpMatch(url, \"http://img*.kanpani.jp/img/quest/chapter_title/*\"))\n" +
                "    return 'PROXY localhost:8899';\n" +
                "  return 'DIRECT';\n" +
                "}"
      }};
      chrome.proxy.settings.set(
          {value: config, scope: 'regular'},
          function() {});