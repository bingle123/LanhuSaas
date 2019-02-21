console.log('init');
(function($) {
    $.fn.extend({
        dataflow: function(options) {
            var _self = this;
            var _this = $(this);
            var defaults = {
                lineWidth: 2, // 线的宽度 默认为2
                lineHoverColor: 'red', // 高亮颜色
                defaultColor: '#61B7CF', // 默认颜色
                lineRadius: 5, // 线拐弯弧度
                pointColor: 'rgba(0,0,0,0.5)', // 端点的颜色
                pointWidth: 5, // 连接端点的半径
                pointDistance: 8, // 端点与线的距离
                data: {}, // 渲染的数据源
                id: 'chart', // 配置渲染的节点id
                isEdit: true, // 是否可配置模版
                canvas: null, // 画布
                dropElevent: null, // 拖拽的数据源
                template: null, // 可配置的模版
                arrowHeight: 7, // 箭头高度
                arrowWidth: 5, // 箭头宽度
                onRemoveNodeAfter: function(a, b) {}, // 删除节点回调,参数为删除节点id和该节点的线条数据
                onCreateNodeAfter: function(a) {}, // 节点创建初始化后事件回调, 参数为节点id
                onCreateLineAfter: function() {}, // 创建线条后事件回调
                ondrawData: function() {} // 渲染流程后回调
            };

            var settings = $.extend({}, defaults, options);

            settings.sourceEndpoint = {
                endpoint: "Dot",
                paintStyle: {
                    stroke: settings.pointColor,
                    fill: settings.pointColor,
                    radius: settings.pointWidth,
                },
                isSource: true,
                isTarget: true,
                connector: [
                    "Flowchart",
                    {
                        stub: [20, 15],
                        gap: settings.pointDistance, // 线离开端点距离
                        cornerRadius: settings.lineRadius,
                        alwaysRespectStubs: true
                    }
                ],
                //描绘线的样式
                connectorStyle: {
                    strokeWidth: settings.lineWidth, // 线条宽度
                    stroke: settings.defaultColor, // 填充颜色
                    joinstyle: "round",
                    outlineWidth: 0 // 线条外部宽度
                },
                dragOptions: {},
                maxConnections: -1 //是否允许多条线
            };

            settings.targetEndpoint = {
                endpoint: "Dot",
                paintStyle: {
                    fill: settings.pointColor,
                    radius: settings.pointWidth
                },
                //描绘线的样式
                connectorStyle: {
                    strokeWidth: settings.lineWidth, // 线条宽度
                    stroke: settings.defaultColor, // 填充颜色
                    joinstyle: "round",
                    outlineWidth: 0 // 线条外部宽度
                },
                maxConnections: -1,
                isSource: true,
                isTarget: true,
                connector: [
                    "Flowchart",
                    {
                        stub: [20, 15],
                        gap: settings.pointDistance,
                        cornerRadius: settings.lineRadius,
                        alwaysRespectStubs: true
                    }
                ]
            };

            // jsplumb插件初始化配置
            var instance = jsPlumb.getInstance({
                Container: "ktj-canvas", // 容器id
                //配置链接线的样式
                ConnectionOverlays: [
                    ["Arrow", {
                        location: 1, // 箭头方向 0-1
                        width: settings.arrowHeight, // 箭头高度
                        length: settings.arrowWidth, // 箭头宽度
                        id: "amrrow",
                        foldback: 1,
                        events: {
                            click: function(e) {
                                e.stopPropagation();
                            }
                        }
                    }],
                ]
            });

            var opt = {
                // 拖动插入的模块
                initHtml: function(options) {
                    var str = options.str.replace(/\{\w+\}/i, options.id);
                    var id = '#' + options.id;
                    var data = {
                        id: id,
                        str: str
                    };
                    return data;
                },
                // 获取流程的个数
                getId: function() {
                    var _window = $(settings.canvas).find('.jtk-window');
                    var num = _window.length;
                    var arr = [];
                    for (var i = 0; i < num; i++) {
                        var str = $(_window).eq(i).attr('id');
                        arr.push(str.substring(str.length - 1));
                    }

                    if (arr.length == 0) {
                        arr.push(0)
                    };
                    var _num = Math.max.apply(null, arr);
                    return _num;
                },
                //获取流程的名字
                getName: function(obj) {
                    var name = $(obj).attr('data');
                    return name;
                }
            };

            var init = function() {
                var self = _this;
                var isMove = false;
                var currentNode = null;
                var _html = null;
                var _obj = null; //是否按下就放开
                self.off();
                var $template = $(settings.template);
                self.on('mousedown', settings.el, function(e) {
                    var __this = $(this);
                    if (!settings.isEdit) {
                        return false;
                    }
                    e.preventDefault(); //禁止移动时出现选择
                    var type = __this.attr('data-type');
                    var obj = $template.find('.jtk-window');
                    $(obj).each(function(val, el) {
                        if ($(el).attr('data-type') == type) {
                            _html = el.outerHTML;
                        }
                    });
                    $('body').append(_html);
                    var top = $('body').scrollTop();
                    var x = e.pageX + 10;
                    var y = e.pageY + 10;
                    currentNode = $('body >.jtk-window');
                    $(currentNode).css({
                        left: x,
                        top: y,
                        position: 'fixed',
                        opacity: '0.7',
                        'z-index': 9999,
                        'background': '#fafafa',
                    })
                    isMove = true;
                })
                    .on('mousemove', function(e) {
                        var top = $('body').scrollTop();
                        _obj = $('body >.jtk-window').length;
                        if (isMove) {
                            $(currentNode).css({
                                left: e.pageX + 10 + 'px',
                                top: e.pageY + 10 - top + 'px'
                            });
                        }
                    })
                    .on('mouseup', function(e) {
                        if (isMove && _obj && settings.isEdit) {
                            var obj = opt.initHtml({
                                id: settings.id + (opt.getId() + 1),
                                str: _html
                            });

                            var canvas = $(settings.canvas);
                            var scroll_top = canvas.scrollTop(); //画布纵向滚动高度
                            var scroll_left = canvas.scrollLeft(); //画布横向滚动高度
                            var w = parseInt(canvas.width());
                            var h = parseInt(canvas.height());
                            var left = canvas.offset().left;
                            var top = canvas.offset().top;

                            var _x = e.pageX - (left + scroll_left);
                            var _y = e.pageY - (top + scroll_top);
                            if (_x < 0 || _x > w || _y < 0 || _y > h) {
                                $('body >.jtk-window').remove('*');
                                return false;
                            };
                            canvas.append(obj.str);

                            $(obj.id).css({
                                left: e.pageX + 10 - left + scroll_left + 'px',
                                top: e.pageY + 10 - top + scroll_top + 'px'
                            });
                            $('body >.jtk-window').remove('*');
                            // 初始化流程
                            _addPointsData(instance); //增加一个流程时重新绘制
                        } else {
                            $('body >.jtk-window').remove('*');
                        }
                        isMove = false;
                    });

                if (Object.keys(settings.data).length > 0) {
                    _drawData(settings.data)
                };

                // 鼠标右键事件
                document.getElementById(settings.canvas.substring(1)).oncontextmenu = function() {
                    return false
                };

                $(settings.canvas).on('mousedown', '.jtk-window', function(e) {
                    e = e || event;
                    var id = $(this).attr('id');
                    // 右键
                    if (e.which == 3 && settings.isEdit) {
                        e.stopPropagation();
                        var x = e.pageX + 10;
                        var y = e.pageY + 10;
                        $('.jtk-delete').css({
                            left: x,
                            top: y,
                            display: 'block'
                        });
                        $('.jtk-delete').off();
                        $('.jtk-delete').on('click', function(e) {
                            e.stopPropagation();
                            _deleteData(id, settings.onRemoveNodeAfter);
                            $('.jtk-delete').css('display', 'none');
                        })
                    };

                });
                $('body').click(function(e) { //隐藏右键弹窗事件
                    $('.jtk-delete').css('display', 'none');
                });
            };

            // 初始化jsplumb插件
            jsPlumb.fire("jsPlumbDemoLoaded", instance);

            /*
             *	删除节点
             *	回调参数为删除节点的id, 与当前节点相关的线数据，可根据此数据找出与删除节点相连的节点
             */
            var _deleteData = function(id, callback) {
                var line = _self.data('dataflow').getLinesByNodeId(id);
                var conn = instance.connect({
                    source: id,
                    target: 'xxxxxx'
                });
                instance.remove(id);
                if (typeof callback === 'function' && callback) {
                    callback(id, line);
                }
            };

            /*
            *	如果有数据，则初始化流程节点, 绑定事件
            */
            var _drawData = function(data) {
                instance.batch(function() {
                    if (data && Object.keys(data).length > 0) {
                        var template = $(settings.template);
                        for (var s = 0; s < data.location.length; s++) {
                            var str = opt.initHtml({
                                id: data.location[s].id,
                                str: template.find("[data-type=" + data.location[s].type + "]")[0].outerHTML
                            });
                            $(settings.canvas).append(str.str);
                            $(str.id).find('p').text(data.location[s].name);
                            $(str.id).css({
                                left: data.location[s].x + 'px',
                                top: data.location[s].y + 'px'
                            });
                        }
                    }

                    var windows = jsPlumb.getSelector(settings.canvas + ' ' + '.jtk-window'); //获取流程对象；

                    _hightLight(windows);
                    _dataConnect(instance, data);

                    //拖动连线结束时触发
                    instance.bind("connectionDragStop", function(connection) {
                        if (connection.sourceId == connection.targetId) {
                            instance.detach(connection);
                        };
                        settings.onCreateLineAfter(connection);
                    });

                    //拖动线前触发
                    instance.bind("connectionDrag", function(conn) {
                        if (!settings.isEdit) {
                            instance.detach(conn);
                            settings.onCreateLineBefore(conn);
                            return false;
                        };
                    })

                    // 所有div流程都可拖动
                    if (settings.isEdit) {
                        // 点击连线
                        instance.bind("dblclick", function(conn, originalEvent) {
                            instance.detach(conn); //删除连线
                        });
                        instance.draggable(jsPlumb.getSelector(settings.canvas + ' ' + '.jtk-window'), {
                            grid: [20, 20]
                        });
                    };
                    settings.ondrawData();
                });
            };

            /*
            *	数据连线
            */
            var _dataConnect = function(instance, data) {
                var windows = jsPlumb.getSelector(settings.canvas + ' ' + '.jtk-window');
                var windowsLength = windows.length;
                for (var i = 0; i < windowsLength; i++) {
                    _addEndpoints(instance, $(windows[i]).attr('id'), ["Top", "Bottom"], ["Left", "Right"]);
                    // 执行回调
                    if (typeof settings.onCreateNodeAfter === 'function') {
                        settings.onCreateNodeAfter($(windows[i]).attr('id'));
                    }
                }

                if (data && Object.keys(data).length > 0) {
                    for (var s = 0, l = data.line.length; s < l; s++) {
                        instance.connect({
                            source: data.line[s].source.id,
                            target: data.line[s].target.id,
                            uuids: [data.line[s].source.arrow + data.line[s].source.id, data.line[s].target.arrow + data.line[s].target.id],
                            type: "Flowchart"
                        })
                    }
                }
            };

            // 绑定高亮事件
            var _hightLight = function(obj) {
                var flag = false;
                $(obj).off();
                $(obj).on('mouseover', function(e) {
                    var id = $(this).attr('id');
                    var dataflow = _self.data('dataflow');
                    var line = dataflow.getLinesByNodeId(id);
                    _toggleColor(line, settings.lineHoverColor);
                })
                    .on('mousedown', function() {
                        flag = true;
                    })
                    .on('mousemove', function() {
                        // if (flag) {
                        //     var id = $(this).attr('id');
                        //     var dataflow = _self.data('dataflow');
                        //     var line = dataflow.getLinesByNodeId(id);
                        //     _toggleColor(line, settings.defaultColor);
                        // }

                    })
                    .on('mouseup', function() {
                        flag = false;
                    })
                    .on('mouseout', function(e) {
                        var id = $(this).attr('id');
                        var dataflow = _self.data('dataflow');
                        var line = dataflow.getLinesByNodeId(id);
                        _toggleColor(line, settings.defaultColor);
                    });
            };

            // 流程节点mouseout高亮
            var _toggleColor = function(arr, color) {
                var self = this;
                var l = arr.length;
                for (var i = 0; i < l; i++) {
                    $(arr[i].canvas).find('path').css({
                        fill: color,
                        stroke: color
                    });
                }
            };

            // 添加一个流程节点，使节点可拖拽
            var _addPointsData = function(instance) {
                instance.batch(function() {
                    var windows = jsPlumb.getSelector(settings.canvas + ' ' + '.jtk-window'); //获取流程对象；
                    var windowsLength = windows.length - 1;

                    _addEndpoints(instance, $(windows[windowsLength]).attr('id'), ["Top", "Bottom"], ["Left", "Right"]);
                    instance.draggable(jsPlumb.getSelector(settings.canvas + ' ' + '.jtk-window'), {
                        grid: [20, 20]
                    });

                    // 绑定双击节点时，高亮与节点相关的所有线条
                    _hightLight(windows);

                    if (typeof settings.onCreateNodeAfter === 'function') {
                        settings.onCreateNodeAfter($(windows[windowsLength]).attr('id'));
                    }

                })
            };

            // 初始化流程节点，使节点添加端点
            var _addEndpoints = function(instance, toId, sourceAnchors, targetAnchors) {
                var self = this;
                for (var i = 0; i < sourceAnchors.length; i++) {
                    var sourceUUID = sourceAnchors[i] + toId;
                    instance.addEndpoint(toId, settings.sourceEndpoint, {
                        anchor: sourceAnchors[i],
                        uuid: sourceUUID
                    });
                };
                for (var j = 0; j < targetAnchors.length; j++) {
                    var targetUUID = targetAnchors[j] + toId;
                    instance.addEndpoint(toId, settings.targetEndpoint, {
                        anchor: targetAnchors[j],
                        uuid: targetUUID
                    })
                }
            };


            // dataflow初始化
            var dataflow = function(obj) {
                init.call(this);
            };

            /*
            *	id为DOM节点 id
            *	type为线的类型，可选 source，target，默认为 all
            *	返回与节点相关的 全部/出发点/终点 的数据
            */
            dataflow.prototype.getLinesByNodeId = function(id, type) {
                if (!(arguments.length > 0)) {
                    return 'getLinesByNodeId(id, type)必须传递节点id参数';
                };
                var id = id,
                    type = type || 'all';
                var allLine = this.getLines();
                var line = allLine.filter(function(val, index) {
                    switch (type) {
                        case 'all':
                            if (id == val.sourceId || id == val.targetId) {
                                return val;
                            };
                            break;
                        case 'source':
                            if (id == val.sourceId) {
                                return val;
                            };
                            break;
                        case 'target':
                            if (id == val.targetId) {
                                return val;
                            }
                            break;
                        default:
                            return 'getLinesByNodeId(id, type)必须传递节点id参数';
                            break;
                    }
                });
                return line;
            };

            /*
            *	获取所有的线条数据
            */
            dataflow.prototype.getLines = function() {
                var c = this.instance.getAllConnections();
                return c;
            };

            /*
            *	将插件对象添加至原型，可查询插件的配置
            */
            dataflow.prototype.instance = instance;

            dataflow.prototype.getAllData = function() {
                var list = this.instance.getAllConnections();
                // 保存线
                var p = false;
                if (list.length == 0) {
                    var p = confirm('节点还没创建连线！')
                };
                if (p) {
                    return false;
                };
                var line = list.map(function(val, index) {
                    return {
                        source: {
                            id: val.endpoints[0].anchor.elementId,
                            arrow: val.endpoints[0].anchor.type
                        },
                        target: {
                            id: val.endpoints[1].anchor.elementId,
                            arrow: val.endpoints[1].anchor.type
                        }
                    }
                });
                // 保存位置
                var connectionPosition = [];
                $(settings.canvas + ' ' + '.jtk-window').each(function(index, el) {
                    var elem = $(el);
                    connectionPosition.push({
                        id: elem.attr('id'),
                        x: parseInt(elem.css('left')),
                        y: parseInt(elem.css('top')),
                        name: elem.attr('node-title').val(),
                        type: elem.attr('data-type')
                    })
                });
                var result = {
                    line: line,
                    location: connectionPosition
                };
                return result;

            };

            /*
            *	设置某一个节点
            *	{options，x/y可选，设置默认值为15px，type类型为必选项}
            *	x: 新增节点的x坐标，y: 新增节点的y坐标，type: 新增节点的模版类型
            */
            dataflow.prototype.setNode = function(options) {
                var $template = $(settings.template);
                var tem = $template.find('.jtk-window');
                var _html = '';
                $(tem).each(function(val, el) {
                    if ($(el).attr('data-type') == options.type) {
                        _html = el.outerHTML;
                    }
                });
                var obj = opt.initHtml({
                    id: settings.id + (opt.getId() + 1),
                    str: _html
                });
                var canvas = $(settings.canvas);
                canvas.append(obj.str);
                $(obj.id).css({
                    left: options.x || 15 + 'px',
                    top: options.y || 15 + 'px'
                });
                _addPointsData(instance);

            };

            /*
             *	连接指定的线；数组的第一个参数为节点id、第二个参数为节点的端点位置, Left, Right, Top, Bottom
             *	数据格式
             *	{
             *		source: ['ch3','Top'],
             * 		target: ['ch2', 'Bottom']
             * 	}
             */
            dataflow.prototype.setLine = function(options) {
                instance.connect({
                    source: options.source[0],
                    target: options.target[0],
                    uuids: [options.source[1] + options.source[0], options.target[1] + options.target[0]],
                    type: "Flowchart"
                })

            };

            /*
             *	重置画布
             */
            dataflow.prototype.resetCanvas = function() {
                settings.data = {};
                var win = $(settings.canvas).find('.jtk-window');
                var _l = win.length;
                for (var i = 0; i < _l; i++) {
                    this.deleteNode($(win).eq(i).attr('id'))
                };
            };

            /*
             *	删除某个节点
             *	{id}
             */
            dataflow.prototype.deleteNode = function(id) {
                _deleteData(id);
            };

            return $.each(this, function() {
                var $this = $(this);
                if (!$this.data('dataflow')) {
                    $this.data('dataflow', new dataflow($this));
                }
            });
        }
    })
})(jQuery)
