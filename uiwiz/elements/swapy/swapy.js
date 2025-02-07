const containers = document.querySelectorAll('#swapy')
var swapies = [];

containers.forEach((container) => {
    const swapy = Swapy.createSwapy(container)
    swapies.push(swapy)
});

class CusSwapy {
    constructor(element) {
        this._element = element;
        this.swapy = Swapy.createSwapy(element);
        this.init();
    }

    init() {

    }

    destroy() {
        this.swapy.destroy();
    }
}

class MyButton {
    constructor(element) {
        this.element = element;
        this.count = 0;
        this.init();
    }

    init() {
        this.element.addEventListener("click", () => {
            this.count++;
            this.update();
        });
        this.update();
    }

    update() {
        this.element.textContent = `Click count: ${this.count}`;
    }
}

// init buttons
document.querySelectorAll(".my-button").forEach((button) => {
    new MyButton(button);
});