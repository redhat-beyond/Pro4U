var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],

    offset: 'bottom-in-view',

    onBeforePageLoad: function () {
    console.log('Before page load');
        $('.loading').show();
    },
    onAfterPageLoad: function () {
    console.log('After page load');
        $('.loading').hide();
    }
});