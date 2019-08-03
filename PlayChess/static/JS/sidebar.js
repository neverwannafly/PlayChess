jQuery(function ($) {

    // Dropdown menu
    $(".sidebar-dropdown > a").click(function () {
        $(".sidebar-submenu").slideUp(200);
        if ($(this).parent().hasClass("active")) {
            $(".sidebar-dropdown").removeClass("active");
            $(this).parent().removeClass("active");
        } else {
            $(".sidebar-dropdown").removeClass("active");
            $(this).next(".sidebar-submenu").slideDown(200);
            $(this).parent().addClass("active");
        }

    });

    //toggle sidebar overlay
    $("#overlay").click(function () {
        $(".page-wrapper").toggleClass("toggled");
    });

    // toggle background image
    $("#toggle-bg").change(function (e) {
        e.preventDefault();
        $('.page-wrapper').toggleClass("sidebar-bg");
    });

    // toggle border radius
    $("#toggle-border-radius").change(function (e) {
        e.preventDefault();
        $('.page-wrapper').toggleClass("boder-radius-on");
    });

});

function makeSideBarToggable() {
    if ($(".page-wrapper").hasClass("pinned")) {
        // unpin sidebar when hovered
        $(".page-wrapper").removeClass("pinned");
        $("#sidebar").unbind( "hover");
    } else {
        $(".page-wrapper").addClass("pinned");
        $("#sidebar").hover(
            function () {
                $(".page-wrapper").addClass("sidebar-hovered");
            },
            function () {
                $(".page-wrapper").removeClass("sidebar-hovered");
            }
        )
    }
    $(".page-wrapper").addClass("pinned");
}

function makeSideBarStatic() {
    $(".page-wrapper").removeClass("pinned");
}

// Manage sidebar in accordance with screen size
let sideBarManager = function() {
    if (window.innerWidth > 531 && window.innerWidth <= 787) {
        makeSideBarToggable();
    } else {
        makeSideBarStatic();
    }
}

window.addEventListener("resize", sideBarManager);
window.addEventListener("onload", sideBarManager);