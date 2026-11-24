import QtQuick

Item {
    property string name: ""
    property int size: 18

    implicitWidth: size
    implicitHeight: size

    Image {
        anchors.fill: parent
        source: "icons/" + name + ".svg"
        fillMode: Image.PreserveAspectFit
        smooth: true
        opacity: 1
    }
}
