function changeState(btn1_id, btn2_id, input1_id, input2_id) {
    let btn1_radio, btn2_radio, input1, input2
    btn1_radio = document.getElementById(btn1_id)
    btn2_radio = document.getElementById(btn2_id)
    input1 = document.getElementById(input1_id)
    input2 = document.getElementById(input2_id)
    if (btn1_radio.checked) {
        input1.removeAttribute("disabled")
        input2.setAttribute("disabled", "")
    }

    if (btn2_radio.checked) {
        input2.removeAttribute("disabled")
        input1.setAttribute("disabled", "")
    }
}
function editPost(btn_el, id, url) {

    btn_el.setAttribute("hidden", true)

    let div_el, right_button, body_el, text_el, submit_el, content

    div_el = document.getElementById(id)
    body_el = document.getElementById(id).children[0]
    content = body_el.innerHTML

    text_el = document.createElement("textarea")
    text_el.setAttribute("rows", "4")
    text_el.setAttribute("name", "new_body")
    text_el.value = content

    right_button = document.createElement("div")
    right_button.setAttribute("class", "button-right")

    submit_el = document.createElement("button")
    submit_el.setAttribute("type", "submit")
    submit_el.setAttribute("class", "btn btn-outline-primary")
    submit_el.innerHTML = "Applica"

    div_el.removeChild(body_el)
    div_el.appendChild(text_el)
    div_el.appendChild(right_button)
    right_button.appendChild(submit_el)

    submit_el.onclick = function() {

        let data
        data = {"new_body": text_el.value}
        $(document).ready(function() {
            $.post(url, data, function(result) {

                let div_flashed_message
                body_el.innerHTML = result

                div_flashed_message = document.createElement("div")
                div_flashed_message.setAttribute("class", "alert alert-info")
                div_flashed_message.innerHTML = "Commento modificato con successo!"

                right_button.removeChild(submit_el)
                div_el.removeChild(right_button)
                div_el.removeChild(text_el)
                div_el.appendChild(body_el)
                div_el.appendChild(div_flashed_message)
                btn_el.removeAttribute("hidden")

            })
        })
    }
}

function alertDeletingProfile(delete_profile_url) {
    if (confirm("Sei sicuro di voler cancellare il tuo account? Non potrai più tornare indietro.")) {
        window.location.href = delete_profile_url
    } else {
      // Non fare niente!
    }
}
function textFormatting(id) {
    let textBody, content, highlighted
    textBody = document.getElementById("article-body")
    highlighted = window.getSelection().toString()
    content = textBody.value
    if (id === "bold") {
        if (highlighted) {
            textBody.value = content.replace(highlighted, "<b>" + highlighted + "</b>")
        } else {
            textBody.value = content + "<b></b>"
        }
    } else if (id === "italic") {
        if (highlighted) {
            textBody.value = content.replace(highlighted, "<i>" + highlighted + "</i>")
        } else {
            textBody.value = content + "<i></i>"
        }
    } else if (id === "underline") {
        if (highlighted) {
            textBody.value = content.replace(highlighted, "<u>" + highlighted + "</u>")
        } else {
            textBody.value = content + "<u></u>"
        }
    }
}

function showPreview(article_date) {
    let div_container
    // form html
    let article_title, article_subtitle, article_body, article_img
    // contenuti form
    let title_content, subtitle_content, body_content, url
    // elementi html per la visualizzazione dei contenuti finora inseriri
    let preview_title, preview_subtitle, preview_data, preview_body, preview_img
    let d, month, day, output1, hours, minutes, output2

    div_container = document.getElementById("preview-container")

    article_title = document.getElementById("article-title")
    article_subtitle = document.getElementById("article-subtitle")
    article_body = document.getElementById("article-body")
    article_img = document.getElementById("image-url")

    title_content = article_title.value
    subtitle_content = article_subtitle.value
    body_content = article_body.value
    url = article_img.value

    preview_title = document.getElementById("title-preview")
    preview_subtitle = document.getElementById("subtitle-preview")
    preview_body = document.getElementById("body-preview")
    preview_img = document.getElementById("img-preview")
    preview_data = document.getElementById("data-preview")

    preview_title.innerHTML = title_content
    preview_subtitle.innerHTML = subtitle_content
    preview_body.innerHTML = body_content + " " + url
    preview_img.setAttribute("src", url)

    if (article_date==="None") {
        d = new Date()
        month = d.getMonth()+1
        day = d.getDate()
        output1 = (day<10 ? "0" : "") + day + "/" + (month<10 ? "0" : "") + month + "/" + d.getFullYear()
        minutes = d.getMinutes()
        hours = d.getHours()
        output2 = (hours<10 ? "0" : "") + hours + ":" + (minutes<10 ? "0" : "") + minutes
        preview_data.innerHTML = "Articolo pubblicato il: " + output1 + ", alle ore: " + output2
    }
    else {
        preview_data.innerHTML = article_date
    }

    div_container.removeAttribute("style")
}

function fallBackIMG(el) {
    el.setAttribute("src", "/static/logo/fallback_img.jpg")
}