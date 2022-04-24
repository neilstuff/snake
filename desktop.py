# Tutorial example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+

from cefpython3 import cefpython as cef
import base64

# HTML code. Browser will navigate to a Data uri created
# from this html code.
HTML_code = """
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Dr Neil's Stuff</title>
    
    <style type="text/css">
        ul.tree,
        ul.tree ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            padding-left: 7px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            cursor: default;
        }

        hr {
            display: block;
            height: 1px;
            border: 0;
            background-color: rgba(0, 0, 0, 0.02);
            border-top: 2px dashed rgba(0, 0, 0, 0.2);
            margin: 1em 0;
            padding: 0;
            height: 1px;
            width: 100px;
        }

        li.last {
            background-repeat: no-repeat;
        }

        ul.tree ul {
            padding-left: 7px;
        }

        ul.tree li {
            margin: 0;
            padding: 0 12px;
            padding-right: 0px;
            line-height: 24px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }

        ul.tree li.last {}

        img.exp_col {
            position: absolute;
            margin-top: 4px;
            margin-left: -20px;
            vertical-align: sub;
        }

        img.exp_col_empty {
            position: absolute;
            margin-top: 4px;
            margin-left: -20px;
            vertical-align: sub;
            width: 16px;
        }

        img.icon_tree {
            vertical-align: middle;
            padding-left: 3px;
            margin-top: -3px;
        }

        a.node {
            padding: 2px;
        }

        span.node a {
            padding-left: 3px;
        }

        span.node {
            margin-left: -1px;
            padding-right: 3px;
            padding-top: 4px;
            padding-bottom: 4px;
        }

        span.node:hover {
            margin-left: -1px;
            padding-right: 3px;
            padding-top: 4px;
            padding-bottom: 4px;
            background-color: #DCEDFF;
        }

        span.node_selected {
            margin-left: -2px;
            padding-right: 3px;
            padding-top: 4px;
            padding-bottom: 4px;
            background-color: #CEFFCE;
            border: 1px solid #8AE88A;
            border-radius: 2px;
        }

        span.node_dragover {
            margin-left: -1px;
            padding-right: 3px;
            padding-top: 4px;
            padding-bottom: 4px;
            background-color: #DCEDFF;
            border-radius: 2px;
        }

        span.node_selected a {
            padding-left: 3px;
        }

        .menu,
        .sub-menu {
            margin: 0;
            padding: 0;
            font: 10px Verdana, sans-serif;
        }

        .menu,
        .sub-menu {
            list-style: none;
            background: #000;
        }

        .sub-menu {
            background: #F1F1F1;
        }

        .menu a {
            text-decoration: none;
            display: inline-block;
            padding: 8px;
        }

        .menu span {
            position: absolute;
            width: 100%;
            height: 100%;
        }

        .menu div {
            position: absolute;
            right: 4px;
            top: 0px;
            padding: 8px;
        }

        .menu .menu_img {
            vertical-align: middle;
        }

        .menu img {
            text-decoration: none;
            display: inline-block;
            vertical-align: sub;
            padding-left: 5px;
        }

        .menu li {
            position: relative;
        }

        .menu li:hover {
            background: aquamarine;
            cursor: pointer;
        }

        .sub-menu li:hover {
            background: aquamarine;
        }

        .menu li:hover>.sub-menu {
            display: block;
        }

        .menu {
            width: 150px;
            position: absolute;
            background: #F1F1F1;
            -webkit-user-select: none;
            /* Chrome/Safari */
            -moz-user-select: none;
            /* Firefox */
            -ms-user-select: none;
            /* IE10+ */
            cursor: default;
            box-shadow: 2px 2px 3px #BDBDBD;
        }

        .sub-menu {
            display: none;
            position: absolute;
            min-width: 150px;
            box-shadow: 2px 2px 3px #BDBDBD;
        }

        .menu .sub-menu {
            top: 0;
            left: 100%;
        }
</style>

<style type="text/css">

    .modal {
        font-size: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        position: absolute;
        /* Stay in place */
        z-index: 1001;
        /* Sit on top */
        padding-top: 80px;
        /* Location of the box */
        left: 0px;
        top: 0px;
        right: 0px;
        /* Full width */
        bottom: 0px;
        /* Full width */
        overflow: auto;
        /* Enable scroll if needed */
        opacity: 0.4;
        background-color: white;
        /* Black w/ opacity */
    }


    /* Modal Dimmer */

    .modal-blocker {
        position: absolute;
        padding: 120px;
        top: 0px;
        bottom: 0px;
        left: 0px;
        right: 0px;
        background-color: rgb(0, 0, 0);
        z-index: 1000;
        /* Sit on top */
        opacity: 0.6;
    }


    /* Modal Content */

    .modal-content {
        position: relative;
        margin: auto;
        padding: 0;
        border: 2px solid rgba(0, 0, 0, 0.2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: white;
        width: 70%;
        z-index: 1002;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        -webkit-animation-name: fadeIn;
        -webkit-animation-duration: 0.4s;
        animation-name: fadeIn;
        animation-duration: 0.4s
    }

    .modal-header {
        padding: 2px 6px;
        font-size: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: rgba(0, 0, 0, 0.4);
        color: white;
    }

    .modal-body {
        padding: 2px 16px;
        display: block;
    }

    .modal-btn {
        position: relative;
        font-size: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border: none;
        /* Remove borders */
        color: black;
        border: 2px solid #186904;
        background-color: #a6ff90;
        padding: 6px 14px;
        margin: 4px 2px;
        border-radius: 4px;
        left: -15px;
        cursor: pointer;
        /* Add a pointer cursor on mouse-over */
    }

    .modal-btn:hover {
        opacity: 0.6;
    }

    .modal-cancel-btn {
        position: relative;
        border: none;
        /* Remove borders */
        color: white;
        font-size: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f44336;
        /* Add a backgriund color */
        padding: 6px 14px;
        margin: 4px 2px;
        border-radius: 4px;
        left: -15px;
        cursor: pointer;
        /* Add a pointer cursor on mouse-over */
    }

    .modal-cancel-btn:hover {
        opacity: 0.6;
    }

    .modal-label {
        color: black;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 12px;
    }

    .modal-entry {
        width: 100%;
        /* Full width */
        height: 18px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 14px;
    }


    /* Add animation (fade in the popup) */

    @-webkit-keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }


    /* The Close Button */

    .close {
        color: white;
        float: right;
        font-size: 24px;
    }

    .close:hover,
    .close:focus {
        opacity: 0.6;
        text-decoration: none;
        cursor: pointer;
    }

    .modal-scroll-panel::-webkit-scrollbar-track:vertical {
        width: 8px;
        margin: 1px;
        background: rgba(240, 240, 240, 0.0);
        border-radius: 4px;
    }

    .modal-scroll-panel::-webkit-scrollbar-track:horizontal {
        height: 8px;
        margin: 1px;
        background: rgba(150, 88, 88, 0.0);
        border-radius: 4px;
    }

    .modal-scroll-panel::-webkit-scrollbar {
        width: 8px;
        height: 8px;
        margin: 1px;
        background: rgba(0, 0, 0, 0.0);
        border-radius: 4px;
    }

    .modal-scroll-panel::-webkit-scrollbar-thumb {
        border: 1px solid rgb(134, 134, 134);
        background: rgba(0, 0, 0, 0.05);
        border-radius: 4px;
    }
</style>


<script>
    function createTree(div, backColor, contextMenu, callbacks) {
    var expand_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAP1BMVEUAAACVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpabOh2duAAAAFHRSTlMAAQsOFBheY3h5e4WGiLfD197g6AKE2vwAAAA4SURBVBhXY2DAAlgFmFEF2ESE0US4iBDhxBDhICzCKCjChyLAKyLEhI/PQ4DPjcZnR+MzsPAj8QFk4gLFdH6sXAAAAABJRU5ErkJggg==";
    var collapse_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAOVBMVEUAAACVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaaVpaapFRCOAAAAEnRSTlMABQYQERQVHjthZnBzfo7p6/GnIDUbAAAAR0lEQVQYV53IORaAMAwD0QHCZjZb9z8sDc8EyqjSH2hYX/0OOGJMFz9hVZbi2gBTTAAMrh3ekn5KZTDFclUGkz4G+xlm2ncDeu4CtLEndvMAAAAASUVORK5CYII=";
    var menu_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC23pUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHja7ZdNkuMgDIX3nGKOgCSExHGwgaq5wRx/HoS4O+merpqfxSxiygbL8hPoU0gS+o/vI3zDQUViSGqeS84RRyqpcMXA4+249RTTuu6beB882MP1gGES9HK7zX37V9j17QVL23482oOdW8e30F15C8qMzBhsP99Cwjc77ftQ9ns1vVvOPvXY0fez5/tkSEZT6AkH7kIScc0zisyTpKIXXEkYTniOsSyLiH6eu3ANn5J3jZ5yF+u2y2MqQszbIT/laNtJP8/dytATtXvkhwcmV4gPuRuj+Rj9trqaMjKVw17UfSlrBEekNcl6LaMZTsXYVitojiWeSHoDzQPtDFSIkc1BiRpVGtRXf9KJKSbubOiZTzCYNhfjwqdMBGk2GmxSpAVxcDpBTWDmay604pYV7yRH5EbwZIIYWH5s4TPjn7RLaIxZukTRr1xhXjxrGtOY5OYVXgBCY+dUV35XC+/qJr4DKyCoK82OBdZ43CQOpbfaksVZ4KcxhXgrd7K2BZAixFZMhgQEYiZRyhSN2YiQRwefipmzJD5AgFS5URhgI5IBx3nGxjtGy5eVb2ZsLQChksWApkgFrJQU9WPJUUNVRVNQ1aymrkVrlpyy5pwtzz2qmlgytWxmbsWqiydXz27uXrwWLoItTEsuFoqXUmpF0ArpircrPGo9+JAjHXrkww4/ylFPlM+ZTj3zaaef5ayNmzR8/FtuFpq30mqnjlLqqWvP3br30utArQ0ZaejIw4aPMupFbVN9pEZP5L6mRpvaJJaWn71Rg9nsLkFzO9HJDMQ4EYjbJDA3p8ksOqXEk9xkFgvPTYpBjXTCaTSJgWDqxDroYvdG7ktuQdNvceNfkQsT3b8gFya6Te4jt0+otbq+UWQBmp/CmdMoAxsbHLpX9jq/k/64D38r8BJ6Cb2EXkIvoZfQS+j/ERr48YC/muEn0ZGRG2cGY9UAAAAGYktHRAD/AP8A/6C9p5MAAAAJcEhZcwAAAccAAAHHAcWGGKIAAAAHdElNRQflAwsXISMtbQwkAAAAZ0lEQVQ4y+3RoRGDUBRE0TOfeFxKiMPREnRABVgcjjKgDVyqAIdMDJigGT4y3Jkn352dXf6CCgNesYIaKz5okMYK9ptQIIEQkeiJDiOycLWgGMGMEjnejxOPX7S/TpazM/ZXZrw5YANMWhGO2v5FvgAAAABJRU5ErkJggg==";
    var empty_image = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7";

    function checkParentage(source, target) {

        if (source == null || target == null) {
            return false;
        }

        if (source.id == target.id) {
            return false;
        }

        if (source.childNodes.length == 0) {
            return true;
        }

        let parent = target;

        while (parent != null) {
            if (parent.id == source.id) {

                return false;
            }

            parent = parent.parent;

        }

        return true;

    }

    function createSimpleElement(type, id, className) {
        element = document.createElement(type);
        if (id != undefined) {
            element.id = id;
        }

        if (className != undefined) {
            element.className = className;
        }

        return element;
    }

    function createImgElement(id, className, src, width, height) {
        element = document.createElement('img');
        if (id != undefined) {
            element.id = id;
        }

        if (className != undefined) {
            element.className = className;
        }

        if (src != undefined) {
            element.src = src;
        }

        if (width != undefined) {
            element.style.width = `${width}px`;
        }

        if (height != undefined) {
            element.style.height = `${height}px`;
        }

        return element;

    }

    /**
     * Get an elements position
     * 
     * @param {element} el the elemnt position
     * 
     * @return the x,y coordinates of the element
     */
    function getPosition(el) {
        var xPos = 0;
        var yPos = 0;

        while (el) {
            if (el.tagName == "BODY") {
                // deal with browser quirks with body/window/document and page scroll
                var xScroll = el.scrollLeft || document.documentElement.scrollLeft;
                var yScroll = el.scrollTop || document.documentElement.scrollTop;

                xPos += (el.offsetLeft - xScroll + el.clientLeft);
                yPos += (el.offsetTop - yScroll + el.clientTop);
            } else {
                // for all other non-BODY elements
                xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
                yPos += (el.offsetTop - el.scrollTop + el.clientTop);
            }

            el = el.offsetParent;
        }

        return {
            x: xPos,
            y: yPos
        };
    }

    /**
     * Get the size of the view area
     * 
     * return the size (x,y) of the view area
     * 
     */
    function getWindowSize() {
        var win = window,

            doc = document,
            docElem = doc.documentElement,
            body = doc.getElementsByTagName('body')[0],
            x = win.innerWidth || docElem.clientWidth || body.clientWidth,
            y = win.innerHeight || docElem.clientHeight || body.clientHeight;

        return {
            x: x,
            y: y
        }
    }

    /**
     * Create the Separator
     * @param {element} ulElement 
     * @param {object} tree 
     * @param {object} node 
     */
    function createSeparator(ulElement, tree, node) {
        node.separator = document.createElement('li');
        node.separator.style.height = "2px";
        node.separator.id = `sep-${node.id}`;
        node.separator.ondragover = function(event) {
            for (var i = 0; i < event.dataTransfer.types.length; i++) {
                var type = event.dataTransfer.types[i];
            }

            if (!checkParentage(nodeTree.draggedNode, node)) {
                return false;
            }

            event.preventDefault();

        }

        node.separator.ondragenter = function(event) {

            if (!checkParentage(nodeTree.draggedNode, node)) {
                return false;
            }

            event.preventDefault();
            node.separator.innerHTML = "<hr/>";
            node.separator.style.height = "15px";

        }

        node.separator.ondragleave = function(event) {
            event.preventDefault();
            let data = event.dataTransfer.getData("text");

            node.separator.style.height = "2px";

            while (node.separator.firstChild) {
                node.separator.removeChild(node.separator.firstChild);
            }

        }

        node.separator.ondrop = function(event) {
            event.preventDefault();

            node.separator.style.height = "2px";
            node.separator.innerHTML = "&nbsp;";

            var index = tree.draggedNode.parent.childNodes.indexOf(tree.draggedNode);
            var cloneLi = tree.draggedNode.elementLi.cloneNode(true);

            tree.draggedNode.ulElement.removeChild(tree.draggedNode.separator);

            tree.draggedNode.parent.elementLi.getElementsByTagName("ul")[0].removeChild(tree.draggedNode.elementLi);

            nodeTree.draggedNode.elementLi = cloneLi;
            nodeTree.draggedNode.ulElement = node.ulElement;

            createSeparator(node.ulElement, tree, nodeTree.draggedNode);

            nodeTree.draggedNode.parent.childNodes.splice(index, 1);

            var span = cloneLi.getElementsByTagName("span")[0];
            var images = cloneLi.getElementsByClassName("exp_col");

            decorateNode(tree, nodeTree.draggedNode, span, images[0]);

            node.ulElement.appendChild(cloneLi);

            var separator = document.getElementById(`sep-${node.id}`);

            node.ulElement.insertBefore(tree.draggedNode.separator, separator);
            node.ulElement.insertBefore(cloneLi, separator);

            index = node.parent.childNodes.indexOf(node);
            node.parent.childNodes.splice(index, 0, tree.draggedNode);

            invokeCallack('removechild', tree, tree.draggedNode.parent);

            redrawNode(tree.draggedNode.parent);

            nodeTree.draggedNode = null;

        }

        node.separator.innerHTML = `&nbsp;`;

        ulElement.appendChild(node.separator);

    }

    function decorateNode(tree, node, span, toggleColumn) {

        span.ondblclick = function() {
            if (tree.callbacks && tree.callbacks.hasOwnProperty('ondblclick')) {
                tree.callbacks['ondblclick'](node);
            }
            tree.doubleClickNode(node);
        };

        span.ondragstart = function(event) {

            if (tree.editing) {
                tree.draggedNode = null;
                return;
            }

            tree.draggedNode = node;

            event.dataTransfer.setData("text/plain", node.id);

        };

        span.onclick = function() {

            nodeTree.selectNode(node);

            if (nodeTree.callbacks && nodeTree.callbacks.hasOwnProperty('onclick')) {
                nodeTree.callbacks['onclick'](node);
            }

        };

        span.oncontextmenu = function(e) {
            var showMenu = true;

            if (nodeTree.callbacks && nodeTree.callbacks.hasOwnProperty('oncontextmenu')) {
                showMenu = nodeTree.callbacks['oncontextmenu'](node);
            }

            if (showMenu) {
                nodeTree.selectNode(node);
                nodeTree.nodeContextMenu(e, node);
            }

        };

        span.ondrop = function(event) {

            if (!checkParentage(nodeTree.draggedNode, node)) {
                return false;
            }

            if (nodeTree.callbacks && nodeTree.callbacks.hasOwnProperty('ondrop')) {
                nodeTree.callbacks['ondrop'](event);
            }

            span.style.color = null;

            var index = tree.draggedNode.parent.childNodes.indexOf(tree.draggedNode);
            tree.draggedNode.parent.childNodes.splice(index, 1);

            var parent = tree.draggedNode.parent;

            node.moveChildNode(nodeTree.draggedNode);

            invokeCallack('addchild', tree, node);

            redrawNode(tree.draggedNode.parent);
            redrawNode(parent);

            invokeCallack('addchild', tree, tree.draggedNode.parent);
            invokeCallack('removechild', tree, parent);

            nodeTree.draggedNode = null;

        }

        span.ondragover = function(event) {

            if (!checkParentage(nodeTree.draggedNode, node)) {
                return false;
            }

            event.preventDefault();

            if (tree.callbacks && tree.callbacks.hasOwnProperty('ondropover')) {
                tree.callbacks['ondragover'](event);
            }

            span.style.color = 'rgba(0, 0, 0, 0.2)';

        }

        span.ondragleave = function(event) {
            span.style.color = null;
        }

        toggleColumn.onclick = function() {
            tree.toggleNode(node);
        };

    }

    function invokeCallack(callback, tree, node) {
        if (tree.callbacks && tree.callbacks.hasOwnProperty(callback)) {
            tree.callbacks[callback](node);
        }

    }

    function redrawNode(node) {

        if (node.childNodes.length == 0) {
            var img = node.elementLi.getElementsByTagName("img")[0];

            img.style.visibility = "hidden";
            node.expanded = false;

        }

    }

    var tree = {
        name: 'tree',
        div: div,
        ulElement: null,
        childNodes: [],
        backcolor: backColor,
        contextMenu: contextMenu,
        selectedNode: null,
        draggedNode: null,
        nodeCounter: 0,
        contextMenuDiv: null,
        rendered: false,
        callbacks: callbacks,
        editing: false,
        removeTree: function() {

            while (div.lastElementChild) {
                div.removeChild(treeNode.lastElementChild);
            }

        },

        createNode: function(text, expanded, icon, parentNode, tag, contextMenu) {
            let nodeTree = this;

            node = {
                id: 'node_' + this.nodeCounter,
                text: text,
                icon: icon,
                parent: parentNode,
                expanded: expanded,
                childNodes: [],
                tag: tag,
                contextMenu: contextMenu,
                elementLi: null,
                ulElement: null,
                separator: null,
                removeNode: function() {
                    nodeTree.removeNode(this);
                },
                editNode: function() {
                    nodeTree.editNode(this);
                },
                toggleNode: function(event) {
                    nodeTree.toggleNode(this);
                },
                expandNode: function(event) {
                    nodeTree.expandNode(this);
                },
                expandSubtree: function() {
                    nodeTree.expandSubtree(this);
                },
                setText: function(text) {
                    this.text = text;
                    nodeTree.setText(this, text);
                },
                setIcon: function(icon) {
                    this.icon = icon;
                    nodeTree.setIcon(this, icon);
                },
                selectNode: function() {
                    nodeTree.selectNode(this);
                },
                collapseNode: function() {
                    nodeTree.collapseNode(this);
                },
                collapseSubtree: function() {
                    nodeTree.collapseSubtree(this);
                },
                removeChildNodes: function() {
                    nodeTree.removeChildNodes(this);
                },
                createChildNode: function(text, expanded, icon, tag, contextMenu) {
                    return nodeTree.createNode(text, expanded, icon, this, tag, contextMenu);
                },
                moveChildNode: function(node) {
                    return nodeTree.moveChildNode(this, node);

                }

            }

            this.nodeCounter++;

            if (this.rendered) {
                if (parentNode == undefined) {
                    this.drawNode(this.ulElement, node);
                } else {
                    var v_ul = parentNode.elementLi.getElementsByTagName("ul")[0];
                    var v_img = parentNode.elementLi.getElementsByTagName("img")[0];

                    if (parentNode.childNodes.length == 0) {

                        if (parentNode.expanded) {
                            parentNode.elementLi.getElementsByTagName("ul")[0].style.display = 'block';

                            v_img.style.visibility = "visible";
                            v_img.src = collapse_image;
                            v_img.id = 'toggle_off';
                        } else {
                            parentNode.elementLi.getElementsByTagName("ul")[0].style.display = 'none';
                            v_img.style.visibility = "visible";
                            v_img.src = expand_image;
                            v_img.id = 'toggle_on';
                        }

                    }

                    v_img.style.visibility = "visible";

                    this.drawNode(v_ul, node);

                }
            }

            if (parentNode == undefined) {
                this.childNodes.push(node);
                node.parent = this;
            } else {
                parentNode.childNodes.push(node);
            }

            return node;

        },
        moveChildNode: function(parentNode, childNode) {
            parentNode.elementLi.getElementsByTagName("ul")[0].appendChild(childNode.elementLi);

            parentNode.childNodes.push(childNode);
            var v_img = parentNode.elementLi.getElementsByTagName("img")[0];

            v_img.style.visibility = "visible";

            childNode.parent = parentNode;

        },
        drawTree: function() {
            this.rendered = true;

            var divTree = document.getElementById(this.div);
            divTree.innerHTML = '';

            ulElement = createSimpleElement('ul', this.name, 'tree');
            this.ulElement = ulElement;

            for (var i = 0; i < this.childNodes.length; i++) {
                this.drawNode(ulElement, this.childNodes[i]);
            }

            divTree.appendChild(ulElement);

        },
        drawNode: function(ulElement, node) {
            nodeTree = this;

            var icon = (node.icon == null) ? createImgElement(null, 'icon_tree', empty_image) :
                createImgElement(null, 'icon_tree', node.icon);

            var v_li = document.createElement('li');
            node.elementLi = v_li;
            node.ulElement = ulElement;

            var span = createSimpleElement('span', null, 'node');
            span.draggable = true;

            var toggleColumn = null;

            if (node.childNodes.length == 0) {
                toggleColumn = createImgElement('toggle_off', 'exp_col', collapse_image, 12, 12);
                toggleColumn.style.visibility = "hidden";
            } else {
                toggleColumn = (node.expanded) ? createImgElement('toggle_off', 'exp_col', collapse_image, 12, 12) :
                    createImgElement('toggle_on', 'exp_col', expand_image, 12, 12);
            }

            decorateNode(nodeTree, node, span, toggleColumn);

            span.appendChild(icon);

            v_a = createSimpleElement('a', null, null);
            v_a.innerHTML = `&nbsp;${node.text}`;

            span.appendChild(v_a);

            v_li.appendChild(toggleColumn);
            v_li.appendChild(span);

            if (node.parent.name != 'tree') {
                createSeparator(ulElement, nodeTree, node);
            }

            ulElement.appendChild(v_li);

            var v_ul = createSimpleElement('ul', 'ul_' + node.id, null);
            v_li.appendChild(v_ul);

            if (node.childNodes.length > 0) {

                if (!node.expanded) {
                    v_ul.style.display = 'none';
                }

                for (var iNode = 0; iNode < node.childNodes.length; iNode++) {
                    this.drawNode(v_ul, node.childNodes[iNode]);
                }

            }

        },
        setText: function(node, text) {
            var element = node.elementLi.getElementsByTagName('span')[0].lastChild;
            element.innerHTML = text;
        },
        setIcon: function(node, icon) {
            var element = node.elementLi.getElementsByTagName('span')[0].firstChild;
            element.src = icon;
        },
        expandTree: function() {
            for (var iNode = 0; iNode < this.childNodes.length; iNode++) {
                if (this.childNodes[iNode].childNodes.length > 0) {
                    this.expandSubtree(this.childNodes[iNode]);
                }
            }
        },
        expandSubtree: function(node) {
            this.expandNode(node);
            for (var iNode = 0; iNode < node.childNodes.length; iNode++) {
                if (node.childNodes[iNode].childNodes.length > 0) {
                    this.expandSubtree(node.childNodes[iNode]);
                }
            }
        },
        collapseTree: function() {
            for (var iNode = 0; iNode < this.childNodes.length; iNode++) {
                if (this.childNodes[iNode].childNodes.length > 0) {
                    this.collapseSubtree(this.childNodes[iNode]);
                }
            }
        },
        collapseSubtree: function(node) {
            this.collapseNode(node);
            for (var i = 0; i < node.childNodes.length; i++) {
                if (node.childNodes[i].childNodes.length > 0) {
                    this.collapseSubtree(node.childNodes[i]);
                }
            }
        },
        expandNode: function(node) {

            if (node.childNodes.length > 0 && node.expanded == false) {

                if (this.nodeBeforeOpenEvent != undefined) {
                    this.nodeBeforeOpenEvent(node);
                }

                var img = node.elementLi.getElementsByTagName("img")[0];

                node.expanded = true;

                img.id = "toggle_off";
                img.src = collapse_image;
                elem_ul = img.parentElement.getElementsByTagName("ul")[0];
                elem_ul.style.display = 'block';

                if (this.nodeAfterOpenEvent != undefined) {
                    this.nodeAfterOpenEvent(node);
                }

            }

        },
        collapseNode: function(node) {
            if (node.childNodes.length > 0 && node.expanded == true) {
                var img = node.elementLi.getElementsByTagName("img")[0];

                node.expanded = false;
                if (this.nodeBeforeCloseEvent != undefined) {
                    this.nodeBeforeCloseEvent(node);
                }

                img.id = "toggle_on";
                img.src = expand_image;
                elem_ul = img.parentElement.getElementsByTagName("ul")[0];
                elem_ul.style.display = 'none';

            }
        },
        toggleNode: function(node) {
            if (node.childNodes.length > 0) {
                if (node.expanded) {
                    node.collapseNode();
                } else {
                    node.expandNode();
                }
            }
        },
        resetDragDrop: function() {
            this.draggedNode = null;
        },
        doubleClickNode: function(node) {
            this.toggleNode(node);
        },
        selectNode: function(node) {

            if (!this.rendered) {
                this.selectedNode = node;
                return;
            }

            var span = node.elementLi.getElementsByTagName("span")[0];
            span.className = 'node_selected';

            if (this.selectedNode != null && this.selectedNode != node) {
                this.selectedNode.elementLi.getElementsByTagName("span")[0].className = 'node';
            }

            this.selectedNode = node;

        },
        removeNode: function(node) {
            var index = node.parent.childNodes.indexOf(node);

            node.elementLi.parentNode.removeChild(node.elementLi);
            node.parent.childNodes.splice(index, 1);

            if (node.parent.childNodes.length == 0) {
                var v_img = node.parent.elementLi.getElementsByTagName("img")[0];
                v_img.style.visibility = "hidden";
            }

        },
        removeChildNodes: function(node) {

            if (node.childNodes.length > 0) {
                var v_ul = node.elementLi.getElementsByTagName("ul")[0];

                var v_img = node.elementLi.getElementsByTagName("img")[0];
                v_img.style.visibility = "hidden";

                node.childNodes = [];
                v_ul.innerHTML = "";
            }

        },
        editNode: function(node) {
            function updateNode(node, box, text) {
                text.innerHTML = box.value
                text.style.display = "inline";
                text.style.marginLeft = "4px";

                node.text = box.value;

                node.elementLi.getElementsByTagName("span")[0].className = 'node_selected';
                box.onblur = null;
                box.parentNode.removeChild(box);
                nodeTree.editing = false;

                if (tree.callbacks && tree.callbacks.hasOwnProperty('editnode')) {
                    tree.callbacks['editnode'](node)
                }

            }

            var span = node.elementLi.getElementsByTagName("span")[0];

            var box = document.createElement('input');

            node.elementLi.getElementsByTagName("span")[0].className = 'node';

            var text = node.elementLi.getElementsByTagName('span')[0].lastChild;
            text.innerHTML = "";
            text.style.display = "none";

            box.style.width = "50%";
            node.elementLi.getElementsByTagName('span')[0].appendChild(box);
            box.value = node.text;
            box.focus();
            box.select();
            nodeTree.editing = true;

            box.addEventListener("keyup", function(event) {
                if (event.keyCode == 13) {
                    event.preventDefault();
                    updateNode(node, box, text);

                }
            });

            box.onblur = function(event) {
                event.preventDefault();
                updateNode(node, box, text);
            }

        },
        nodeContextMenu: function(event, node) {
            if (event.button == 2) {
                event.preventDefault();
                event.stopPropagation();

                if (node.contextMenu != undefined) {

                    nodeTree = this;

                    var v_menu = this.contextMenu[node.contextMenu];

                    var v_div;

                    if (this.contextMenuDiv == null) {
                        v_div = createSimpleElement('ul', 'ul_cm', 'menu');
                        document.body.appendChild(v_div);
                    } else {
                        v_div = this.contextMenuDiv;
                    }

                    v_div.innerHTML = '';

                    var v_left = event.pageX - 5;
                    var v_right = event.pageY - 5;

                    var position = getPosition(this.selectedNode.elementLi);
                    var size = getWindowSize();
                    var height = v_menu.elements.length * 40;


                    if (position.y + height > size.y) {
                        position.y = size.y - height;
                    }

                    v_div.style.display = 'block';
                    v_div.style.position = 'absolute';
                    v_div.style.left = (position.x + 6) + 'px';
                    v_div.style.top = (position.y + 27) + 'px';

                    for (var iItem = 0; iItem < v_menu.elements.length; iItem++)(function(iItem) {
                        var v_li = createSimpleElement('li', null, null);
                        var v_span = createSimpleElement('span', null, null);

                        v_span.onclick = function() {
                            v_menu.elements[iItem].action(node)
                        };

                        var v_a = createSimpleElement('a', null, null);
                        var v_ul = createSimpleElement('ul', null, ' sub-menu');

                        v_a.appendChild(document.createTextNode(v_menu.elements[iItem].text));

                        v_li.appendChild(v_span);

                        if (v_menu.elements[iItem].icon != undefined) {
                            var v_img = createImgElement('null', 'null', v_menu.elements[iItem].icon);
                            v_li.appendChild(v_img);
                        }

                        v_li.appendChild(v_a);
                        v_li.appendChild(v_ul);
                        v_div.appendChild(v_li);

                        if (v_menu.elements[iItem].submenu != undefined) {
                            var v_span_more = createSimpleElement('div', null, null);
                            v_span_more.appendChild(createImgElement(null, 'menu_img', menu_image, 16, 16));
                            v_li.appendChild(v_span_more);
                            nodeTree.contextMenuListItem(v_menu.elements[iItem].submenu, v_ul, node);
                        }

                    })(iItem);

                    this.contextMenuDiv = v_div;

                }
            }
        },
        contextMenuListItem: function(submenu, p_ul, p_node) {
            nodeTree = this;

            for (var iSubmenu = 0; iSubmenu < submenu.elements.length; iSubmenu++)(function(iSubmenu) {
                var v_li = createSimpleElement('li', null, null);
                var v_span = createSimpleElement('span', null, null);

                v_span.onclick = function() {
                    submenu.elements[iSubmenu].action(p_node)
                };

                var v_a = createSimpleElement('a', null, null);
                var v_ul = createSimpleElement('ul', null, 'sub-menu');

                v_a.appendChild(document.createTextNode(submenu.elements[iSubmenu].text));

                v_li.appendChild(v_span);

                if (submenu.elements[iSubmenu].icon != undefined) {
                    var v_img = createImgElement('null', 'null', submenu.elements[iSubmenu].icon);
                    v_li.appendChild(v_img);
                }

                v_li.appendChild(v_a);
                v_li.appendChild(v_ul);
                p_ul.appendChild(v_li);

                if (submenu.elements[iSubmenu].p_submenu != undefined) {
                    var v_span_more = createSimpleElement('div', null, null);
                    v_span_more.appendChild(createImgElement(null, 'menu_img', menu_image, 16, 16));
                    v_li.appendChild(v_span_more);
                    nodeTree.contextMenuListItem(submenu.elements[iSubmenu].p_submenu, v_ul, p_node);
                }

            })(iSubmenu);
        }

    }

    window.onclick = function() {
        if (tree.contextMenuDiv != null) {
            tree.contextMenuDiv.style.display = 'none';
        }
    }

    return tree;

}
</script>
    <style type="text/css">
        .menu {
            color: #888888;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
        }
        
        .menu:hover {
            color: #444444;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
            cursor: pointer
        }
        
        .menu-selected {
            color: #000000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
        }
        
        .cardbox {
            margin-top: 64x;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            width: 100%;
            height: 100%;
            justify-content: left;
            box-sizing: border-box;
        }
        
        .card {
            width: 90px;
            height: 90px;
            font-size: 10px;
            margin: 10px;
            color: rgba(255, 255, 255, 1.0);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: rgb(255, 255, 255);
            cursor: pointer
        }
        
        .card:hover {
            background-color: rgb(229, 243, 255);
        }
        
        .card img {
            display: block;
            margin-top: 4px;
            margin-left: auto;
            margin-right: auto;
            width: 60px;
            height: 60px;
        }
        
        .card label {
            display: block;
            width: 100%;
            color: black;
            font-size: 12px;
            text-align: center;
            overflow: hidden;
            margin-top: 0px;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
        
        .details {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 5px;
        }
        
        .center {
            border-top: 2px solid #DDDDDD;
            border-bottom: 2px solid #DDDDDD;
            text-align: center;
        }
        
        .float-left {
            width: 480px;
            height: 480px;
            margin: 20px;
            float: left;
        }
        
        kbd.key {
            border-radius: 3px;
            padding: 1px 2px 0;
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            border: 1px solid black;
        }
        
         ::-webkit-scrollbar-track:vertical {
            width: 12px;
            background: rgba(240, 240, 240, 0.05);
            border-radius: 4px;
        }
        
         ::-webkit-scrollbar-track:horizontral {
            height: 12px;
            background: rgba(240, 240, 240, 0.05);
            border-radius: 4px;
        }
        
         ::-webkit-scrollbar {
            width: 11px;
            background: rgba(0, 0, 0, 0.05);
            border-radius: 5px;
        }
        
         ::-webkit-scrollbar-thumb {
            border: 1px solid rgb(134, 134, 134);
            background: rgba(0, 0, 0, 0.05);
            border-radius: 5px;
        }
    </style>
    <script type="text/template" id="template">
        <div id="card-<%=view%>-<%=repository%>-<%=id%>" class="card" onclick="<%=callback%>('<%=id%>', '<%=repository%>', '<%=view%>');">
            <img src="<%=image%>"></img>
            <label value="<%=label%>"><%=label%></label>
        </div>
    </script>
    <script type="text/template" id="view">
        <div class="details">
            <div class="center">
                <h2>
                    <%=name%>
                </h2>
            </div>
            <div style="position:absolute; top:90px; left:0px; right:0x; bottom: 0px; overflow:auto;">
                <div style="margin:10px;">
                    <div>
                        <p>
                            <%=description%>
                        </p>
                    </div>
                    <div style="margin-top:<%=display%>;">
                        <img src="<%=display%>" style="display:block; <%=border%>; margin-left:auto; margin-right:auto; width:<%=width%>; height:<%=height%>;" </img>
                    </div>
                    <div>
                        <p>
                            <%=notes%>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="pdf">

        <div class="model" id="pdf-view-dialog" style="display:inline-block">
            <div style="position:absolute; padding:120px; top:0px; bottom:0px; left:0px; right:0px;">
                <div class="modal-content" style="margin-top:40px; width:730px; height:600px">
                    <div class="modal-header" style="background-color: black ">
                        <span class="close" id="close" onclick="close_model_panel()">&times;</span>
                        <h2 id="pdf-dialog_title ">PDF Viewer</h2>
                    </div>
                    <div class="modal-body" style="background: rgba(0,0,0,0.0.5);">
                        <iframe id="pdf-viewer" src="<%=file%>" title="webviewer" frameborder="0" width="700" height="540"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="player">
        <div class="model" id="player-dialog" style="display:inline-block">
            <div style="position:absolute; padding:120px; top:0px; bottom:0px; left:0px; right:0px; background: light-grey;">
                <div class="modal-content" style="margin-top:20px; width:<%=width%>px; height:<%=height%>px;">
                    <div class="modal-header " style="background-color: black ">
                        <span class="close" id="close" onclick="close_model_panel()">&times;</span>
                        <h2 id="viewer-dialog_title">
                            <%=title%>
                        </h2>
                    </div>
                    <div class="modal-body" style="background: rgba(0,0,0,0.0.5); margin-top:8px; margin-left:auto; margin-right:auto;">
                        <iframe id="player-viewer" src="<%=url%>" title="player" frameborder="0" width="<%=viewport-width%>" height="<%=viewport-height%>" style="transform:scale(<%=scale%>); margin-top:<%=margin-top%>px;  margin-left:<%=margin-left%>px;"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </script>

    <script type="text/template" id="notifications">
        <div class="details" style="position:absolute; top:4px; bottom:0px; left:0px; right:0px;">
            <div class="center">
                <h2>What's Here</h2>
            </div>
            <div style="position:absolute; top:90px; left:0px; right:0x; bottom: -50px; overflow:auto;">
                <div style="margin:10px;">
                    <ul>
                        <li>Applications and Utilities</li>
                        <li>Knowledge Archives</li>
                        <li>Code Snippets</li>
                        <li>Gameboy <strong>ROMS</strong> (open source only)</li>
                        <li>Notable Publications about Machine, Deep Learning and other stuff</li>
                    </ul>
                    <h4>New Features</h4>
                    <ul>
                        <li>New version of <strong>Electron Pipe</strong> with full inhibitor arc support.</li>
                        <li>Full support of Yatt archives with an Azure Machine Learning Pipleline.</li>
                        <li>All <b>Electron</b> applications have both a Mac and Windows installer. Linux is comming!</li>
                        <li>If you ar Macintosh Classic fan - there will be instructions on how to <b>recap</b> 1989 these ancient machines.</li>
                        <li>New games added: daleks (classic Macintosh Game) and ski-free (classic Windows Game).</li>

                    </ul>
                    <h4>Dr. Neil's Publications</h4>
                    <ul>
                        <li>Dr. Neil's Thesis - <a href="documents/thesis.pdf">Schema Last Approach</a></li>
                    </ul>
                </div>
            </div>
    </script>

    <script>
        /*  Tables and Lists*/

        var repositories = [];
        var views = [];
    </script>
    <script>
        function play(name, url, height, width, scale) {
            var element = document.getElementById("player");

            var template = element.text;
            var adjustment = parseFloat(scale);
            var adjustedWidth = parseInt(width) * adjustment
            var adjustedHeight = parseInt(height) * adjustment

            var viewportWidth = parseInt(width) - 30;
            var viewportHeight = parseInt(height) - 70;
            var marginTop = 0;
            var marginLeft = 0;

            if (adjustment != 1.0) {
                marginTop = (height - adjustedHeight) * scale;
                marginLeft = (width - adjustedWidth) * scale;

                marginTop -= 15;
                adjustedHeight += 30;

            }

            var html = template.replace('<%=url%>', url).
            replace('<%=title%>', name).
            replace('<%=width%>', adjustedWidth).
            replace('<%=height%>', adjustedHeight).
            replace('<%=viewport-width%>', viewportWidth).
            replace('<%=viewport-height%>', viewportHeight).
            replace('<%=scale%>', parseFloat(scale)).
            replace('<%=margin-top%>', '-' + marginTop).
            replace('<%=margin-left%>', '-' + marginLeft);

            document.getElementById('viewer').innerHTML = html;

        }

        function display(definitions, view, callback, filter, repository) {
            var element = document.getElementById("template");
            var template = element.text;
            var cardValue = "";

            for (definition in definitions) {
                if (filter == '*' || filter == definitions[definition].category) {
                    cardValue += template.replace(/<%=callback%>/g, callback).
                    replace(/<%=image%>/g, definitions[definition].image).
                    replace(/<%=label%>/g, definitions[definition].label).
                    replace(/<%=repository%>/g, repository).
                    replace(/<%=view%>/g, view).
                    replace(/<%=id%>/g, definition);
                }
            }
            var card = document.getElementById(view);

            card.innerHTML = cardValue;

        }

        function show(file) {
            var element = document.getElementById("pdf");
            var template = element.text;

            var html = template.replace('<%=file%>', file);

            document.getElementById('viewer').innerHTML = html;

        }

        function displayDetails(id, repositoryId, view) {
            var element = document.getElementById("view");
            var template = element.text;
            var entry = parseInt(id);
            var repository = repositories[parseInt(repositoryId)];
            var description = "";

            for (var line in repository[entry].description) {
                description += repository[entry].description[line];
            }

            var html = template.replace(/<%=name%>/g, repository[entry].label).
            replace(/<%=description%>/g, description);

            if ('display' in repository[entry]) {
                html = html.replace(/<%=display%>/g, repository[entry].display.image);
                html = html.replace(/<%=width%>/g, repository[entry].display.width);
                html = html.replace(/<%=height%>/g, repository[entry].display.height);
                html = html.replace(/<%=border%>/g, repository[entry].display.border);
                html = html.replace(/<%=margin%>/g, repository[entry].display.margin);
            }

            var notes = "";

            if ('notes' in repository[entry]) {
                for (var note in repository[entry].notes) {
                    notes += repository[entry].notes[note];
                }

            }

            html = html.replace(/<%=notes%>/g, notes);

            var details = document.getElementById("details");

            details.innerHTML = html;

            var github = document.getElementById("github");

            if ('github' in repository[entry]) {
                github.href = `javascript:window.open('${repository[entry].github}', '_blank').focus(); `;
                github.style.display = 'inline-block';
            } else {
                github.style.display = 'none';
            }

            var download = document.getElementById("download");
            var show = document.getElementById("show");

            show.style.display = 'none';
            download.style.display = 'none';

            if ('download' in repository[entry]) {

                if (typeof repository[entry].download === 'string') {
                    download.style.display = 'inline';
                    download.href = repository[entry].download;
                } else if (navigator.platform in repository[entry].download) {
                    download.style.display = 'inline';
                    download.href = repository[entry].download[navigator.platform];
                } else if ('type' in repository[entry].download && repository[entry].download.type == 'pdf') {
                    show.style.display = 'inline';
                    show.href = `javascript:show("${repository[entry].download.file}")`;
                } else {
                    download.style.display = 'none';
                }

            } else {
                download.style.display = 'none';
            }

            var play = document.getElementById("play");

            if ('play' in repository[entry]) {
                play.style.display = 'inline';
                play.href = `javascript:play("${repository[entry]['label']}", ` +
                    `"${repository[entry]['play']['index']}", ` +
                    `"${repository[entry]['play']['size']['height']}", ` +
                    `"${repository[entry]['play']['size']['width']}", ` +
                    `"${repository[entry]['play']['scale']}")`;

            } else {
                play.style.display = 'none';
            }

            document.getElementById("actions").style.display = "inline-block";

            var elements = document.getElementsByClassName("card");
            for (var element = 0; element < elements.length; element++) {
                elements[element].style.cssText = "";
            }

            document.getElementById(`card-${view}-${repositoryId}-${id}`).style.cssText =
                "color:red; background-color:rgb(206, 255, 206);";

        }

        document.addEventListener("DOMContentLoaded", (event) => {

            var CALLBACKS = {

                onclick: function(node) {

                    function show(id) {
                        var items = document.getElementsByClassName('view');

                        for (var item = 0; item < items.length; item++) {

                            if (items[item].id == id) {
                                items[item].style.display = "inline-block"
                            } else {
                                items[item].style.display = "none"
                            }

                        }

                    }

                    document.getElementById("details").innerHTML = "";
                    document.getElementById("actions").style.display = "none";

                    var elements = document.getElementsByClassName("card");
                    for (var element = 0; element < elements.length; element++) {
                        elements[element].style.cssText = "";
                    }

                    if (node.text == 'Stuff') {

                        show('stuff');

                        var notifications = document.getElementById("notifications").text;

                        document.getElementById("details").innerHTML = notifications;

                    } else if (node.text in views) {

                        show(views[node.text]);

                    }

                },

                addchild: function(node) {},

                removechild: function(node) {},

                editnode: function(node) {},

                oncontextmenu: function(node) {
                    return false;
                }

            }

            repositories[APPLICATIONS] = applications;
            repositories[ARCHIVES] = archives;
            repositories[DOCUMENTS] = documents;
            repositories[PROJECTS] = projects;

            views['Applications'] = 'cards';
            views['Games'] = 'games';
            views['Utilities'] = 'utilities';
            views['Examples'] = 'examples';
            views['Archives'] = 'knowledge';
            views['Azure'] = 'azure';
            views['Projects'] = 'projects';
            views['Library'] = 'documents';

            var tree = createTree("menu", 'white', null, CALLBACKS);

            var root = tree.createNode('Stuff', true, 'icons/folder-icon.png', null, null, null);
            var applicationNode = root.createChildNode('Applications', true, 'icons/application.png', null, null);

            applicationNode.createChildNode('Games', true, 'icons/games.png', null, null);
            applicationNode.createChildNode('Utilities', true, 'icons/utilities.png', null, null);
            applicationNode.createChildNode('Examples', true, 'icons/examples.png', null, null);

            var projectNode = root.createChildNode('Projects', true, 'icons/projects.png', null, null);
            var knowledgeNode = root.createChildNode('Archives', true, 'icons/knowledge-archives.png', null, null);

            knowledgeNode.createChildNode('Azure', false, 'icons/azure.png', null, null);
            root.createChildNode('Library', true, 'icons/lego.png', null, null);

            tree.drawTree();

            display(applications, 'cardbox', 'displayDetails', '*', APPLICATIONS);
            display(applications, 'gamebox', 'displayDetails', 'Game', APPLICATIONS);
            display(applications, 'utilitybox', 'displayDetails', 'Utility', APPLICATIONS);
            display(applications, 'examplebox', 'displayDetails', 'Example', APPLICATIONS);
            display(projects, 'projectbox', 'displayDetails', '*', PROJECTS);
            display(archives, 'knowledgebox', 'displayDetails', '*', ARCHIVES);
            display(archives, 'azurebox', 'displayDetails', 'Azure', ARCHIVES);
            display(documents, 'documentbox', 'displayDetails', '*', DOCUMENTS);

            var notifications = document.getElementById("notifications").text;

            document.getElementById("details").innerHTML = notifications;

            root.selectNode();

        });
    </script>
    <script>
        function help() {
            document.getElementById('help-dialog').style.display = "inline-block";
        }

        function close_model_panel() {
            var dialogs = document.getElementsByClassName('model')

            for (var dialog in dialogs) {
                if (dialogs[dialog].style) {
                    dialogs[dialog].style.display = "none";
                }

            }
        }
    </script>
</head>

<body style=" overflow:hidden">
    <div style="position:absolute; top:0px; height:60px; left:0px; right:0px; background-color:rgb(36,41,46)">
        <div style="position:absolute; top:-4px; left:10px; font-size:48px;">&#129490;</div>
        <div style="position:absolute; top:-2px; height:60px; left:80px; right:0px; background-color:rgb(36,41,46)">
            <h1 style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #FFFFFF; font-size:24px;">
                &nbsp;Dr.&nbsp;Neil's - Home of Stuff - Desktop</h1>
        </div>
        <div style="position:absolute; top:18px; height:60px; right:4px;">
            <a href="javascript:help()" style="cursor:pointer; margin-top:-4px; margin-left:10px; width:16px; height:16px;">
                <svg style="width: 24px; height: 24px;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 96C0 78.33 14.33 64 32 64H416C433.7 64 448 78.33 448 96C448 113.7 433.7 128 416 128H32C14.33 128 0 113.7 0 96zM0 256C0 238.3 14.33 224 32 224H416C433.7 224 448 238.3 448 256C448 273.7 433.7 288 416 288H32C14.33 288 0 273.7 0 256zM416 448H32C14.33 448 0 433.7 0 416C0 398.3 14.33 384 32 384H416C433.7 384 448 398.3 448 416C448 433.7 433.7 448 416 448z" fill="white"/></svg>
            </a>
        </div>
    </div>
    <div id="menu" style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size:14px; margin:10px; position:absolute; top:60px; left:0px; bottom:0px; width:190px; padding:5px; border: 1px solid rgba(0, 0, 0, 0.2);">
    </div>
    <div id="stuff" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); background-color: rgb(255, 255, 255); ">
 
    </div>
    <div id="cards" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="cardbox" class="cardbox"> </div>
    </div>
    <div id="knowledge" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="knowledgebox" class="cardbox"> </div>
    </div>
    <div id="games" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="gamebox" class="cardbox"> </div>
    </div>
    <div id="utilities" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="utilitybox" class="cardbox"> </div>
    </div>
    <div id="examples" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="examplebox" class="cardbox"> </div>
    </div>
    <div id="documents" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="documentbox" class="cardbox"> </div>
    </div>
    <div id="projects" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="projectbox" class="cardbox"> </div>
    </div>
    <div id="azure" class="view" style="position: absolute; top: 70px; bottom: 10px; left: 220px; right: 310px; border: 1px solid rgba(0, 0, 0, 0.2); flex-wrap: wrap; align-content: flex-start; background-color: rgb(255, 255, 255); overflow: auto; display:none;">
        <div id="azurebox" class="cardbox"> </div>
    </div>
    <div id="summary" style="position:absolute; top: 70px; bottom:10px; width:290px; right:10px; border:1px solid rgba(0,0,0,0.2);	background-color:rgb(255, 255, 255);">
    </div>
    <div class="model" id="help-dialog" style="display:none">
        <div style="position:absolute; padding:120px; top:0px; bottom:0px; left:0px; right:0px;">
            <div class="modal-content" style="margin-top:40px; width:540px;">
                <div class="modal-header" style="background-color: black">
                    <span class="close" id="close" onclick="close_model_panel()">&times;</span>
                    <h2 id="dialog_title">Stuff you need to know</h2>
                </div>
                <div class="modal-body" id="text" style="background: rgba(0,0,0,0.0.5); height:400px;">
                    <div id="getting_started_panel" class="modal-scroll-panel" style="position:absolute; top:50px; bottom:36px; left:0px; right:0px; overflow:auto; ">
                        <table style="margin:5px;" cellpadding="10">
 
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="viewer">
    </div>

</body>

</html>
"""

def js_print(browser, lang, event, msg):
    browser.ExecuteFunction("js_print", lang, event, msg)

def html_to_data_uri(html):
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    return ret

def main():

    WIDTH = 1300    
    HEIGHT = 840

    cef.Initialize({
        'context_menu' : {
            'enabled': True
        }
    })
    
    window_info = cef.WindowInfo()
    parent_handle = 0

    browser = cef.CreateBrowserSync(url=html_to_data_uri(HTML_code),
                                    window_info=window_info,
                                    window_title="Desktop Stuff")
    cef.MessageLoop()
    del browser
    cef.Shutdown()

if __name__ == '__main__':
    main()