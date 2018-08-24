/**
 * Created by Administrator on 2018-6-25.
 */

function IronSSHClient(){

}

IronSSHClient.prototype._generateURl = function (options) {
    if (window.location.protocol == "https") {
        var protocol = "wss://";
    }else {
        var protocol = "ws://";
    }

    var url = protocol + window.location.host + "/host/" + encodeURIComponent(options.des_id) + "/";
    return url;
};


IronSSHClient.prototype.connect = function (options) {
    var des_url = this._generateURl(options);

    if (window.WebSocket){
        this._connection = new WebSocket(des_url);
    }
    else if (window.MozWebSocket){
        this._connection = new MozWebSocket(des_url);
    }
    else {
        options.onError("当前浏览器不支持WebSocket");
        return;
    }
    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = JSON.parse(evt.data.toString());
        console.log(evt,data);
        if (data.error !== undefined){
            options.onError(data.error);
        }
        else {
            options.onData(data.data);
        }

    };

    // this._connection.onmessage = function (evt) {
    //
    //     // var data = JSON.parse(evt.data.toString());
    //     if (data.error !== undefined){
    //         options.onError(data.error);
    //     }
    //     else {
    //         options.onCopy(data.data);
    //     }
    // };

    this._connection.onclose = function (evt) {
        options.onClose();
    };
};


IronSSHClient.prototype.send = function (data) {

    this._connection.send(JSON.stringify({'data':data}));

};