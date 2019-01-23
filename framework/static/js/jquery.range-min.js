!function ($, t, i, s) {
    "use strict";
    var o = function () {
        return this.init.apply(this, arguments)
    };
    o.prototype = {
        defaults: {
            onstatechange: function () {
            },
            ondragend: function () {
            },
            onbarclicked: function () {
            },
            isRange: !1,
            showLabels: !0,
            showScale: !0,
            step: 1,
            format: "%s",
            theme: "theme-green",
            width: 300,
            disable: !1,
            snap: !1
        },
        template: '<div class="slider-container">			<div class="back-bar">                <div class="selected-bar"></div>                <div class="pointer low"></div><div class="pointer-label low">123456</div>                <div class="pointer high"></div><div class="pointer-label high">456789</div>                <div class="clickable-dummy"></div>            </div>            <div class="scale"></div>		</div>',
        init: function (t, i) {
            this.options = $.extend({}, this.defaults, i), this.inputNode = $(t), this.options.value = this.inputNode.val() || (this.options.isRange ? this.options.from + "," + this.options.from : "" + this.options.from), this.domNode = $(this.template), this.domNode.addClass(this.options.theme), this.inputNode.after(this.domNode), this.domNode.on("change", this.onChange), this.pointers = $(".pointer", this.domNode), this.lowPointer = this.pointers.first(), this.highPointer = this.pointers.last(), this.labels = $(".pointer-label", this.domNode), this.lowLabel = this.labels.first(), this.highLabel = this.labels.last(), this.scale = $(".scale", this.domNode), this.bar = $(".selected-bar", this.domNode), this.clickableBar = this.domNode.find(".clickable-dummy"), this.interval = this.options.to - this.options.from, this.render()
        },
        render: function () {
            return 0 !== this.inputNode.width() || this.options.width ? (this.options.width = this.options.width || this.inputNode.width(), this.domNode.width(this.options.width), this.inputNode.hide(), this.isSingle() && (this.lowPointer.hide(), this.lowLabel.hide()), this.options.showLabels || this.labels.hide(), this.attachEvents(), this.options.showScale && this.renderScale(), void this.setValue(this.options.value)) : void console.log("jRange : no width found, returning")
        },
        isSingle: function () {
            return "number" == typeof this.options.value ? !0 : -1 === this.options.value.indexOf(",") && !this.options.isRange
        },
        attachEvents: function () {
            this.clickableBar.click($.proxy(this.barClicked, this)), this.pointers.on("mousedown touchstart", $.proxy(this.onDragStart, this)), this.pointers.bind("dragstart", function (t) {
                t.preventDefault()
            })
        },
        onDragStart: function (t) {
            if (!(this.options.disable || "mousedown" === t.type && 1 !== t.which)) {
                t.stopPropagation(), t.preventDefault();
                var s = $(t.target);
                this.pointers.removeClass("last-active"), s.addClass("focused last-active"), this[(s.hasClass("low") ? "low" : "high") + "Label"].addClass("focused"), $(i).on("mousemove.slider touchmove.slider", $.proxy(this.onDrag, this, s)), $(i).on("mouseup.slider touchend.slider touchcancel.slider", $.proxy(this.onDragEnd, this))
            }
        },
        onDrag: function (t, i) {
            i.stopPropagation(), i.preventDefault(), i.originalEvent.touches && i.originalEvent.touches.length ? i = i.originalEvent.touches[0] : i.originalEvent.changedTouches && i.originalEvent.changedTouches.length && (i = i.originalEvent.changedTouches[0]);
            var s = i.clientX - this.domNode.offset().left;
            this.domNode.trigger("change", [this, t, s])
        },
        onDragEnd: function (t) {
            this.pointers.removeClass("focused").trigger("rangeslideend"), this.labels.removeClass("focused"), $(i).off(".slider"), this.options.ondragend.call(this, this.options.value)
        },
        barClicked: function (t) {
            if (!this.options.disable) {
                var i = t.pageX - this.clickableBar.offset().left;
                if (this.isSingle()) this.setPosition(this.pointers.last(), i, !0, !0); else {
                    var s = Math.abs(parseFloat(this.pointers.first().css("left"), 10)),
                        o = this.pointers.first().width() / 2,
                        e = Math.abs(parseFloat(this.pointers.last().css("left"), 10)),
                        n = this.pointers.first().width() / 2, a = Math.abs(s - i + o), h = Math.abs(e - i + n), l;
                    l = a == h ? s > i ? this.pointers.first() : this.pointers.last() : h > a ? this.pointers.first() : this.pointers.last(), this.setPosition(l, i, !0, !0)
                }
                this.options.onbarclicked.call(this, this.options.value)
            }
        },
        onChange: function (t, i, s, o) {
            var e, n;
            e = 0, n = i.domNode.width(), i.isSingle() || (e = s.hasClass("high") ? parseFloat(i.lowPointer.css("left")) + i.lowPointer.width() / 2 : 0, n = s.hasClass("low") ? parseFloat(i.highPointer.css("left")) + i.highPointer.width() / 2 : i.domNode.width());
            var a = Math.min(Math.max(o, e), n);
            i.setPosition(s, a, !0)
        },
        setPosition: function (t, i, s, o) {
            var e, n, a = parseFloat(this.lowPointer.css("left")), h = parseFloat(this.highPointer.css("left")) || 0,
                l = this.highPointer.width() / 2;
            if (s || (i = this.prcToPx(i)), this.options.snap) {
                var r = this.correctPositionForSnap(i);
                if (-1 === r) return;
                i = r
            }
            t[0] === this.highPointer[0] ? h = Math.round(i - l) : a = Math.round(i - l), t[o ? "animate" : "css"]({left: Math.round(i - l)}), this.isSingle() ? e = 0 : (e = a + l, n = h + l);
            var d = Math.round(h + l - e);
            this.bar[o ? "animate" : "css"]({
                width: Math.abs(d),
                left: d > 0 ? e : e + d
            }), this.showPointerValue(t, i, o), this.isReadonly()
        },
        correctPositionForSnap: function (t) {
            var i = this.positionToValue(t) - this.options.from,
                s = this.options.width / (this.interval / this.options.step), o = i / this.options.step * s;
            return o + s / 2 >= t && t >= o - s / 2 ? o : -1
        },
        setValue: function (t) {
            var i = t.toString().split(",");
            i[0] = Math.min(Math.max(i[0], this.options.from), this.options.to) + "", i.length > 1 && (i[1] = Math.min(Math.max(i[1], this.options.from), this.options.to) + ""), this.options.value = t;
            var s = this.valuesToPrc(2 === i.length ? i : [0, i[0]]);
            this.isSingle() ? this.setPosition(this.highPointer, s[1]) : (this.setPosition(this.lowPointer, s[0]), this.setPosition(this.highPointer, s[1]))
        },
        renderScale: function () {
            for (var t = this.options.scale || [this.options.from, this.options.to], i = Math.round(100 / (t.length - 1) * 10) / 10, s = "", o = 0; o < t.length; o++) s += '<span style="left: ' + o * i + '%">' + ("|" != t[o] ? "<ins>" + t[o] + "</ins>" : "") + "</span>";
            this.scale.html(s), $("ins", this.scale).each(function () {
                $(this).css({marginLeft: -$(this).outerWidth() / 2})
            })
        },
        getBarWidth: function () {
            var t = this.options.value.split(",");
            return t.length > 1 ? parseFloat(t[1]) - parseFloat(t[0]) : parseFloat(t[0])
        },
        showPointerValue: function (t, i, o) {
            var e = $(".pointer-label", this.domNode)[t.hasClass("low") ? "first" : "last"](), n,
                a = this.positionToValue(i);
            if ($.isFunction(this.options.format)) {
                var h = this.isSingle() ? s : t.hasClass("low") ? "low" : "high";
                n = this.options.format(a, h)
            } else n = this.options.format.replace("%s", a);
            var l = e.html(n).width(), r = i - l / 2;
            r = Math.min(Math.max(r, 0), this.options.width - l), e[o ? "animate" : "css"]({left: r}), this.setInputValue(t, a)
        },
        valuesToPrc: function (t) {
            var i = 100 * (parseFloat(t[0]) - parseFloat(this.options.from)) / this.interval,
                s = 100 * (parseFloat(t[1]) - parseFloat(this.options.from)) / this.interval;
                i = 100
                s = 200
            return [i, s]
        },
        prcToPx: function (t) {
            return this.domNode.width() * t / 100
        },
        isDecimal: function () {
            return -1 !== (this.options.value + this.options.from + this.options.to).indexOf(".")
        },
        positionToValue: function (t) {
            var i = t / this.domNode.width() * this.interval;
            if (i = parseFloat(i, 10) + parseFloat(this.options.from, 10), this.isDecimal()) {
                var s = Math.round(Math.round(i / this.options.step) * this.options.step * 100) / 100;
                if (0 !== s) for (s = "" + s, -1 === s.indexOf(".") && (s += "."); s.length - s.indexOf(".") < 3;) s += "0"; else s = "0.00";
                return s
            }
            return Math.round(i / this.options.step) * this.options.step
        },
        setInputValue: function (t, i) {
            if (this.isSingle()) this.options.value = i.toString(); else {
                var s = this.options.value.split(",");
                t.hasClass("low") ? this.options.value = i + "," + s[1] : this.options.value = s[0] + "," + i
            }
            this.inputNode.val() !== this.options.value && (this.inputNode.val(this.options.value).trigger("change"), this.options.onstatechange.call(this, this.options.value))
        },
        getValue: function () {
            return this.options.value
        },
        getOptions: function () {
            return this.options
        },
        getRange: function () {
            return this.options.from + "," + this.options.to
        },
        isReadonly: function () {
            this.domNode.toggleClass("slider-readonly", this.options.disable)
        },
        disable: function () {
            this.options.disable = !0, this.isReadonly()
        },
        enable: function () {
            this.options.disable = !1, this.isReadonly()
        },
        toggleDisable: function () {
            this.options.disable = !this.options.disable, this.isReadonly()
        },
        updateRange: function (t, i) {
            var s = t.toString().split(",");
            this.interval = parseInt(s[1]) - parseInt(s[0]), i ? this.setValue(i) : this.setValue(this.getValue())
        }
    };
    var e = "jRange";
    $.fn[e] = function (i) {
        var s = arguments, n;
        return this.each(function () {
            var a = $(this), h = $.data(this, "plugin_" + e), l = "object" == typeof i && i;
            h || (a.data("plugin_" + e, h = new o(this, l)), $(t).resize(function () {
                h.setValue(h.getValue())
            })), "string" == typeof i && (n = h[i].apply(h, Array.prototype.slice.call(s, 1)))
        }), n || this
    }
}(jQuery, window, document);