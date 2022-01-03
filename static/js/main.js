soundManager.setup({
    url: '/static/swf/',
    flashVersion: 9,
    debugFlash: false,
    debugMode: false,
    useHTML5Audio: true,
    preferFlash: false,
    forceUseGlobalHTML5Audio: true,
    flashLoadTimeout: 0,
    ontimeout: function() {
        // console.log('SM2 init failed!');
    },
    ontimeout: function() {
        // console.log('SM2 init failed!');
    },
    defaultOptions: {
        // set global default volume for all sound objects
        volume: 95
      }
});

var file, id, oldId, oldFile, player = false;
play_ids = [];

audio_obj = {
    playing_id: null,
    state: 'stop',
    last_play_id: null,
};
var apiUrl = 'https://7nota.kz/api/audio-detail/'

function getUrl(id)
{
     var result = null
     $.ajax({
        url: apiUrl+id,
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(data) {
            result = data;
        } 
     });
     return result.file;
}
$(function () {
    play_ids = [];
    $('.play').each(function () {
        var id = $(this).attr('id');
        play_ids.push(id);
    });

    $('.play').click(function (event) {
        var id = $(this).attr('id');
        var file_url = getUrl(id)
        play(id, file_url);
        event.preventDefault();
    });
});

function bind_play_buttons() {

    play_ids = [];
    $('.play').each(function () {
        $(this).unbind('click');
        var id = $(this).attr('id');
        play_ids.push(id);
    });

    $('.play').click(function () {
        var id = $(this).attr('id');
        var file_url = getUrl(id)
        play(id, file_url);
    });
    
}

function getTime(msec, useString) {

    // convert milliseconds to hh:mm:ss, return as object literal or string

    var nSec = Math.floor(msec / 1000),
        hh = Math.floor(nSec / 3600),
        min = Math.floor(nSec / 60) - Math.floor(hh * 60),
        sec = Math.floor(nSec - (hh * 3600) - (min * 60));

    // if (min === 0 && sec === 0) return null; // return 0:00 as null

    return (useString ? ((hh ? hh + ':' : '') + (hh && min < 10 ? '0' + min : min) + ':' + (sec < 10 ? '0' + sec : sec)) : { min: min, sec: sec });

  }

function play(id, file_url) {

    var audio = $('#' + id);
    var audio_id = 'audio' + audio.attr('id');

    if (audio_obj.state == 'play' && audio_obj.playing_id == audio_id) {
        pause(id);
        return;
    }

    if (audio_obj.last_play_id != null && audio_obj.last_play_id != id) {
        stop(audio_obj.last_play_id);
    }

    $('#song' + id).addClass('playing');
    

    if (audio_obj.state == 'pause' && audio_obj.playing_id == audio_id) {
        resume(id);
    }
    else {
        audio_obj.playing_id = audio_id;
        audio_obj.last_play_id = id;
        audio_obj.state = 'play';
        audio.addClass('playing');
        audio.find('span').attr('class', 'spinner-border');


        soundManager.createSound({
            id: 'audio' + id,
            url: file_url,
            onload: function () {
                audio.removeClass('spinner-border');
                audio.find('span').attr('class', 'i i-pause2');
            },

            whileloading: function() {
                $("#load" + id).css('width', ((this.bytesLoaded / this.bytesTotal) * 100) + '%');
            },

            whileplaying: function () {
                $("#progress" + id).css('width', ((this.position / this.duration) * 100) + '%');
                $("#minute" +id).html(getTime(this.position, true));
            },

            onfinish: function () {
            },
        });

        soundManager.play(audio_id, {
            onfinish: function () {
                stop(id);
                var flag_found = false;
                for (var i in play_ids) {
                    if(flag_found == true) {
                        var newId = play_ids[i];
                        break;
                    }

                    if(play_ids[i] == id)
                    {
                        flag_found = true;
                    }
                }
                var newFile = getUrl(newId);
                if (newFile != undefined) {
                    play(newId, newFile);
                }
            }
        });
    }
    $('#seek'+ id).click(function(e){
        // Seek work real server
        var audio_id = 'audio' + id;
        var sound_obj = soundManager.getSoundById(audio_id);

        var posX = $(this).offset().left;
        var pos = Math.min(Math.max((e.pageX - posX) / $(this).width() * 100, 0), sound_obj.duration);
        if(!isNaN(pos) && sound_obj)
        {
            sound_obj.setPosition(Math.round(pos*sound_obj.duration/100));
        }
    });
    
}

function pause(id) {
    var audio = $('#' + id);
    var audio_id = 'audio' + audio.attr('id');

    audio_obj.state = 'pause';
    audio.removeClass('playing');
    audio.find('span').attr('class', 'i i-play2');

    soundManager.pause(audio_id);
}

function resume(id) {

    var audio = $('#' + id);
    var audio_id = 'audio' + id;
    audio_obj.playing_id = audio_id;
    audio_obj.last_play_id = id;
    audio_obj.state = 'play';
    audio.addClass('playing');
    audio.find('span').attr('class', 'i i-pause2');

    soundManager.resume(audio_id);
}

function stop(id) {
    var audio = $('#' + id);
    var audio_id = 'audio' + audio.attr('id');

    $("#progress" + id).css('width', '0');
    var sound_obj = soundManager.getSoundById(audio_id);
    $("#minute" +id).html(getTime(sound_obj.duration, true));

    audio_obj.state = 'stop';
    audio_obj.last_play_id = null;
    audio.removeClass('playing');
    $('#song' + id).removeClass('playing');

    audio.find('span').attr('class', 'i i-play2');

    soundManager.stop(audio_id);
}

