(function(doc, win, $, undefined){
    'use strict';
    dataInit();
    scrollEventBinder($);
    timeCellClickEvent($);
    timeSliceClickEvent($);

    function dataInit(){
        var datetimes = [
            // {
                // "day":0,
                // "date":0,
                // "month":"May",
                // "available":10
            // }
        ];
        var scContainer = doc.querySelectorAll('.date-scroll-container')[0];
        var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for(var i = 0 ; i < 30 ; i++){
            var item = {
                "day":days[i%7],
                "date":i+1,
                "month":"March",
                "available":"10 available"
            }
            scContainer.appendChild(getTemplate(interpolate(i, item)));
        }
    }
    function interpolate(idx, dItem){
        return `<label option-id=${idx} class="timecell">\
            <span class="date-item">
                <input type="radio">\
                <span class="fill-box"></span>\
                <span class="time-day">${dItem.day}</span>\
                <span class="time-date">${dItem.date}</span>\
                <span class="time-month">${dItem.month}</span>\
                <span class="time-available">${dItem.available}</span>\
            </span>
        </label>`;
    }
    function getTemplate(html){
        var template = doc.createElement('template');
        template.innerHTML = html;
        return template.content.firstChild;
    }
    function scrollEventBinder($){
        var dsc = $('.date-scroll-container')[0];
        $('.scroll-btn.left').on('click', function(){
            dsc.scrollLeft -= dsc.clientWidth;
        });
        $('.scroll-btn.right').on('click', function(){
            dsc.scrollLeft += dsc.clientWidth;
        });
    }
    function timeCellClickEvent($){
        var $dp = $('.date-pick');
        $('.timecell').click(function(){
            var sidx = +$dp.attr('data-selected-id');
            if(sidx !== -1){
                $('.timecell[option-id="'+sidx+'"]').removeClass("selected");
            }
            $dp.attr('data-selected-id', $(this).attr("option-id"));
            $(this).addClass('selected');
        });
    }
    function timeSliceClickEvent($){
        var $tp = $('.time-pick');
        $('.time-slice').click(function(){
            var tsidx = +$tp.attr('data-ts-selected-id');
            if(tsidx !== -1){
                $('.time-slice[option-id="'+tsidx+'"]').removeClass("selected");
            }
            $tp.attr('data-ts-selected-id', $(this).attr("option-id"));
            $(this).addClass('selected');
        });
    }

})(document, window, $);