window.onload = function() {
    // PDF 생성
    hGeneratePdfButton.addEventListener("click", async function (e) {
      elems = document.querySelectorAll("input[type=checkbox]:checked");
      if (elems.length == 0) {
        alert("선택된 악보가 없습니다.");
        return;
      }

      const links = [];
      for (let i = 0; i < elems.length; i++) {
        links.push(elems[i].value);
      }

      console.log({ links });

      const blob = await fetch("/api/generate_pdf", {
        method: "POST",
        body: JSON.stringify({
          filelist: links,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => response.blob());

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");

      a.href = url;
      a.download = new Date().toISOString() + ".pdf";

      document.body.appendChild(a);

      a.click();
      document.body.removeChild(a);
    });

    // 검색
    hSearchButton.addEventListener("click", async function (e) {
      console.log("clicked");
      e.preventDefault();

      hSearchResultContainer.innerHTML = "";
      hSongListTableWrapper.innerHTML = "";

      hSpinnerWrapper.classList.remove("hidden");
      hSearchButton.setAttribute("disabled", true);

      let rows = null;

      try {
        rows = await fetch(`/api/analyze_songlist`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt: hInputText.value }),
        }).then((res) => res.json());

        hSpinnerWrapper.classList.add("hidden");
        hSearchButton.removeAttribute("disabled");
      } catch (e) {
        hSpinnerWrapper.classList.add("hidden");
        hSearchButton.removeAttribute("disabled");
        alert("GPT 분석에 실패했습니다.");
        return;
      }

      if (rows && rows.length > 0) {
        tableTag = '<table class="table table-striped"><thead><tr><th>제목</th><th>키</th></tr></thead><tbody>';
        rows.forEach((row) => {
          tableTag += `<tr><td>${row.title}</td><td>${row.key}</td></tr>`;
        });
        tableTag += "</tbody></table>";
        hSongListTableWrapper.innerHTML = `
        <div class="row">
            <div class="col-12">
                <h3>GPT 분석 결과</h3>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                ${tableTag}
            </div>
        </div>
        `;

        try {
          const elems = await Promise.all(
            rows.map(async (row) => {
              console.log(row);
              const elem = await generateImageList(row.title, row.key);
              return elem;
            })
          );

          const container = document.querySelector("#hSearchResultContainer");
          elems.forEach((elem) => container.appendChild(elem));
          hSearchButtonWrapper.classList.remove("hidden");
        } catch (e) {
          alert("이미지 검색에 실패했습니다.");
          return;
        }
      }

      console.log("result", rows);
    });
}

function randomId() {
  return Math.random().toString(36).slice(2, 11);
}

// 검색 결과 생성
async function generateImageList(title, key) {
    r = await fetch(`/api/search?search=${title} ${key} key 악보`)
        .then((res) => res.json())


    const elems = r.items.map((item) => {
        htmlText = `<a href="${item.link}">
            <div class="image-crop"><img src="${item.link}" alt="${item.title}" class="card-img-top" ></div>
        </a>`;
        const myId = randomId()

        wrapperHtmlText = `
        <div class="card" style="width: 440px; height: 540px; padding: 20px">
            ${htmlText}
            <div class="card-body" style="display: flex; flex-direction: column; justify-content: space-between;">
            <h5 class="card-title">${item.title}</h5>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="${item.link}" id="${myId}">
                <label class="form-check-label" for="${myId}">
                    사용하기
                </label>
            </div>
            </div>
        </div>`;

        const li = document.createElement('li');
        li.innerHTML = wrapperHtmlText;
        li.querySelector('img').addEventListener('error', function() {
            li.remove();
        })
        return li;
    })

    const elem = document.createElement('div');
    elem.classList.add('row');
    elem.innerHTML = `
    <div class="col-12 mt-5">
        <div class="container">
            <div class="row">
                <h3>${title} - ${key} key</h3>
            </div>
            <div class="row" style="overflow-x: scroll">
                <ul class="image-list" style="list-style-type: none; display: flex; justify-content: flex-start; gap:20px; flex-wrap: nowrap;"></ul>
            </div>
        </div>
    </div>
    `

    console.log(elem)

    ul = elem.querySelector('ul')
    elems.forEach(elem => ul.appendChild(elem));

    return elem;
}

