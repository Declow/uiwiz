const containers = document.querySelectorAll('#swapy')

swapies = [];

containers.forEach(container => {
    const swapy = Swapy.createSwapy(container);

    swapy.onSwap((event) => {
        console.log(event);
    });
    swapies.push(swapy);
});