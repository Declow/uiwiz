container = document.getElementById("toast");

const observer = new MutationObserver(mutationList =>
    mutationList.filter(m => m.type === 'childList').forEach(m => {
        m.addedNodes.forEach(remove);
    }));

// Configuration of the observer:
var config = {
    attributes: true,
    childList: true,
    characterData: true
};

// Pass in the target node, as well as the observer options
observer.observe(container, config);

function remove(evt) {
    window.setTimeout(() => {
        evt.classList.add('remove');
        evt.style = "--delay: {{ toast_delay - 500 }}ms;";
    }, {{ toast_delay - 500 }});
    window.setTimeout(() => {
        evt.remove();
    }, {{ toast_delay }});
}

function handleInvalidInputs(evt) {
    if (evt.detail.xhr.status == 422) {
        res = JSON.parse(evt.detail.xhr.response);

        res.fieldErrors.forEach(key => {
            evt.target.querySelector(`[name='${key}']`).classList.add("invalid")
        });

        res.fieldOk.forEach(key => {
            evt.target.querySelector(`[name='${key}']`).classList.remove("invalid")
        });
    }
}

document.body.addEventListener('htmx:responseError', function (evt) {
    (function () {
        var container = document.getElementById("toast");
        var error = document.createElement('div');
        error.className = "{{ error_classes }}";
        error.innerHTML = `<span id="a-1">${evt.detail.error}</span>`;
        container.prepend(error);

        handleInvalidInputs(evt);
    }());
});

function handlePreviousInvalidInputsNowValid(evt) {
    if (evt.detail.successful && evt.target.tagName == "FORM") {
        var all = [...evt.target.getElementsByTagName('*')];
        all.forEach(val => {
            if (val.classList.contains("invalid")) {
                val.classList.remove("invalid");
            }
        });
    }
}

document.body.addEventListener("htmx:afterRequest", function (evt) {
    handlePreviousInvalidInputsNowValid(evt);
});

function getAttributeFromElement(element, attrName) {
    return (element.getAttribute(attrName) || element.getAttribute("data-" + attrName));
}

function hasAttribute(element, attrName) {
    return (element.hasAttribute(attrName) || element.hasAttribute("data-" + attrName))
}

htmx.defineExtension('swap-header', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            evt.detail.headers['Hx-Swap'] = getAttributeFromElement(evt.detail.elt, 'hx-swap') || htmx.config.defaultSwapStyle;
        }
    }
});

{% if auth_header_name %}
htmx.on("htmx:afterRequest", (evt) => {
    xhr = evt.detail.xhr;

    if (xhr.getResponseHeader("{{ auth_header_name }}")) {
        let authToken = xhr.getResponseHeader("{{ auth_header_name }}");
        localStorage.setItem("{{ auth_header_name }}", authToken);
    }
});

htmx.on("htmx:configRequest", (evt)=> {
    evt.detail.headers["{{ auth_header_name }}"] = localStorage.getItem("{{ auth_header_name }}");
});
{% endif %}

htmx.on("htmx:configRequest", (evt)=> {
    const urlParams = new URLSearchParams(window.location.search);
    const next = urlParams.get('next');
    if (next) {
        evt.detail.path = evt.detail.path + "?next=" + next
    }
});