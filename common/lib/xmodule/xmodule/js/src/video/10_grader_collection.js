(function (define) {
'use strict';
define(
'video/10_grader_collection.js',
['video/00_abstract_grader.js'],
function (AbstractGrader) {
    /**
     * GraderCollection module.
     * @exports video/10_grader_collection.js
     * @constructor
     * @param {Object} state The object containing the state of the video
     * player.
     * @return {jquery Promise}
     */
    var GraderCollection = function (element, state) {
        if (!(this instanceof GraderCollection)) {
            return new GraderCollection(element, state);
        }

        var hasScore = state.config.hasScore,
            graders = state.config.graders,
            conversions = {
                'scored_on_end': 'GradeOnEnd',
                'scored_on_percent': 'GradeOnPercent'
            };

        return (!hasScore) ? [] : $.map(graders, function (config, name) {
            var graderName = conversions[name],
                Grader = GraderCollection[graderName];

            if (Grader && !config.graderStatus) {
                return new Grader(element, state, config);
            }
        });
    };

    /** Write graders below this line **/

    GraderCollection.GradeOnEnd = AbstractGrader.extend({
        name: 'scored_on_end',

        getGrader: function (element) {
            this.dfd = $.Deferred();

            element.on({
                'ended': this.dfd.resolve,
                'endTime': this.dfd.resolve,
                'ready': this.updateRange.bind(this),
                'play': _.once(this.updateRange.bind(this)),
                'seek': this.onSeekHandler.bind(this)
            });

            return this.dfd.promise();
        },

        updateRange: function (event, time) {
            setTimeout(function () {
                this.range = this.getStartEndTimes();
            }.bind(this), 0);
        },

        onSeekHandler: function (event, time) {
            if (time < this.range.start || this.range.end < time) {
                this.dfd.resolve();
            }
        }
    });

    GraderCollection.GradeOnPercent = AbstractGrader.extend({
        name: 'scored_on_percent',
        size: 100,

        getGrader: function (element, state, config) {
            this.dfd = $.Deferred();
            this.coef = 1;
            this.graderValue = this.config.graderValue + 1;

            if (this.config.graderValue === 0) {
                this.dfd.resolve();
            } else {
                element.on('play', _.once(this.onPlayHandler.bind(this)));
            }

            return this.dfd.promise();
        },

        getProgress: function (timeline) {
            return _.compact(timeline).length * this.coef;
        },

        createTimeline: function (size) {
            // Adds 1 to avoid collisions with interval 0-1.
            return new Array(++size);
        },

        onPlayHandler: function (event) {
            setTimeout(function () {
                var milliseconds, waitTime;

                this.range = this.getStartEndTimes();
                milliseconds = 1000 * this.range.size;
                waitTime = Math.max(milliseconds/100, 1000);

                // In case, when video less than 20 seconds, we receive less
                // than 100 events `progress`(it triggers with interval 200 ms).
                // So, we adjust some settings to make it works well.
                // `this.size` will be equal amount of received events.
                if (milliseconds/waitTime < 100) {
                    this.size = milliseconds/waitTime;
                    this.coef = 100 / this.size;
                }

                this.timeline = this.createTimeline(this.size);

                this.element.on(
                    'progress',
                    _.throttle(
                        this.onProgressHandler.bind(this), waitTime,
                        { leading: false, trailing: true }
                    )
                );
            }.bind(this), 0);
        },

        onProgressHandler: function (event, time) {
            time = Math.floor(time);
            if (this.range.start <= time && time <= this.range.end) {
                var position = Math.floor(this.size * time/this.range.size);

                this.timeline[position] = 1;
                if (this.getProgress(this.timeline) >= this.graderValue) {
                    this.dfd.resolve();
                }
            }
        }
    });

    return GraderCollection;
});

}(window.RequireJS.define));
