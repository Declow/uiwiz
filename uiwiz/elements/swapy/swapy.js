const containers = document.querySelectorAll('#swapy')
var swapies = [];

containers.forEach((container) => {
    const swapy = Swapy.createSwapy(container)
    swapies.push(swapy)
});