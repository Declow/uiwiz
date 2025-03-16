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

function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();
  
    // Change this to div.childNodes to support multiple top-level nodes.
    return div.firstChild;
  }

function remove(evt) {
    // console.log(evt);
    // if (hasAttribute(evt, "hx-toast-data")) {
    //     hxToastData = getAttributeFromElement(evt, "hx-toast-data");
    //     window.setTimeout(() => {
    //         evt.classList.add('remove');
    //         evt.style = "--delay: {{ toast_delay - 500 }}ms;";
    //     }, {{ toast_delay - 500 }});
    //     window.setTimeout(() => {
    //         evt.remove();
    //     }, {{ toast_delay }});
    // }
    // hxToastData = evt.getAttribute("data-hx-toast");
    window.setTimeout(() => {
        evt.classList.add('remove');
        evt.style = "--delay: {{ toast_delay - 500 }}ms;";
    }, {{ toast_delay - 500 }});
    window.setTimeout(() => {
        evt.remove();
    }, {{ toast_delay }});
}

function handleInvalidInputs(evt) {
    if (evt.detail.xhr.getResponseHeader("x-uiwiz-validation-error") === "true") {
        console.log("Validation error");

        var response = createElementFromHTML(evt.detail.xhr.response);
        var res = JSON.parse(getAttributeFromElement(response, "hx-toast-data"));

        res.fieldErrors.forEach(key => {
            var tar = evt.target.querySelector(`[name='${key}']`);
            if (tar != null) {
                tar.classList.add("invalid");
            } else {
                var tar = evt.target.closest("tr");
                var inputElement = tar ? tar.querySelector(`[name='${key}']`) : null;
                if (inputElement != null) {
                    inputElement.classList.add("invalid");
                }
            }
        });

        res.fieldOk.forEach(key => {
            var tar = evt.target.querySelector(`[name='${key}']`)
            if (tar != null) {
                tar.classList.remove("invalid")
            } else {
                var tar = evt.target.closest("tr");
                var inputElement = tar ? tar.querySelector(`[name='${key}']`) : null;
                if (inputElement != null) {
                    inputElement.classList.remove("invalid");
                }
            }
        });
    }
}

function handlePreviousInvalidInputsNowValid(evt) {
    if (evt.detail.successful && evt.target.tagName == "FORM" && evt.detail.xhr.getResponseHeader("x-uiwiz-validation-error") === null) {
        var all = [...evt.target.getElementsByTagName('*')];
        all.forEach(val => {
            if (val.classList.contains("invalid")) {
                val.classList.remove("invalid");
            }
        });
    }
}

document.body.addEventListener("htmx:afterRequest", function (evt) {
    handleInvalidInputs(evt);
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

htmx.on("htmx:configRequest", (evt)=> {
    const urlParams = new URLSearchParams(window.location.search);
    const next = urlParams.get('next');
    if (next) {
        evt.detail.path = evt.detail.path + "?next=" + next
    }
});