(function (define) {
'use strict';
define(
'video/00_abstract_grader.js',
[],
function() {
    /**
     * AbstractGrader module.
     * @exports video/00_abstract_grader.js
     * @constructor
     * @param {Object} state The object containing the state of the video
     * player.
     * @return {jquery Promise}
     */
    var AbstractGrader = function () { };

    /**
     * Returns new constructor that inherits form the current constructor.
     * @static
     * @param {Object} protoProps The object containing which will be added to
     * the prototype.
     * @return {Object}
     */
    AbstractGrader.extend = function (protoProps) {
        var Parent = this,
            Child = function () {
                if ($.isFunction(this.initialize)) {
                    return this.initialize.apply(this, arguments);
                }
            };

        // inherit
        var F = function () {};
        F.prototype = Parent.prototype;
        Child.prototype = new F();
        Child.constructor = Parent;
        Child.__super__ = Parent.prototype;

        if (protoProps) {
            $.extend(Child.prototype, protoProps);
        }

        return Child;
    };

    AbstractGrader.prototype = {
        /** Grader name on backend */
        name: '',

        /** Initializes the module. */
        initialize: function (element, state, config) {
            this.element = element;
            this.state = state;
            this.config = config;
            this.url = this.state.config.gradeUrl;
            this.grader = this.getGrader(this.element, this.state, this.config);

            return this.sendGradeOnSuccess(this.grader);
        },

        /**
         * Factory method that returns instance of needed Grader.
         * @return {jquery Promise}
         * @example:
         *   var dfd = $.Deferred();
         *   this.element.on('play', dfd.resolve);
         *   return dfd.promise();
         */
        getGrader: function (element, state, config) {
            throw new Error('Please implement logic of the `getGrader` method.');
        },

        /**
         * Sends results of grading to the server.
         * @return {jquery Promise}
         */
        sendGrade: function () {
            return $.ajaxWithPrefix({
                url: this.url,
                data: {
                    'graderName': this.name
                },
                type: 'POST',
                notifyOnError: false
            });
        },

        /**
         * Decorates provided grader to send grade results on succeeded scoring.
         * @param {jquery Promise} grader Grader function.
         */
        sendGradeOnSuccess: function (grader) {
            return grader.pipe(this.sendGrade.bind(this));
        },

        /**
         * Returns start/end times for the video.
         * @return {Object} Contains start, end times and size of the interval.
         */
        getStartEndTimes: function () {
            var storage = {
                duration: null,
                range: null
            };

            return function () {
                var startTime = this.state.config.startTime,
                    endTime = this.state.config.endTime,
                    duration = this.state.videoPlayer.duration();

                if (duration === storage.duration && storage.range) {
                    return storage.range;
                } else {
                    storage.duration = duration;
                }

                if (startTime >= duration) {
                    startTime = 0;
                }

                if (endTime <= startTime || endTime >= duration) {
                    endTime = duration;
                }

                if (this.state.isFlashMode()) {
                    startTime /= Number(this.state.speed);
                    endTime /= Number(this.state.speed);
                }

                storage.range = {
                    start: startTime,
                    end: endTime,
                    size: endTime - startTime
                };

                return storage.range;
            };
        }()
    };

    return AbstractGrader;
});
}(RequireJS.define));
