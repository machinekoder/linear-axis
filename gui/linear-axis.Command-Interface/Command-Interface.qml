import QtQuick 2.0
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import Machinekit.Controls 1.0
import Machinekit.HalRemote.Controls 1.0
import Machinekit.HalRemote 1.0

HalApplicationWindow {
    id: main

    name: "command-interface"
    title: qsTr("Command Interface")

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        JointControl { joint: 0 }
        JointControl { joint: 1 }
        JointControl { joint: 2 }
        JointControl { joint: 3 }
        JointControl { joint: 4 }
        JointControl { joint: 5 }
        JointControl { joint: 6 }
        JointControl { joint: 7 }
        JointControl { joint: 8 }
        Item {
            Layout.fillHeight: true
        }
    }
}

