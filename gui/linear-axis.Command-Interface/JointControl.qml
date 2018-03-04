import QtQuick 2.0
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import Machinekit.Controls 1.0
import Machinekit.HalRemote.Controls 1.0
import Machinekit.HalRemote 1.0

RowLayout {
    property int joint: 0
    id: root

    ColumnLayout {
        Layout.fillWidth: true
        HalSlider {
            Layout.fillWidth: true
            name: "joint" + root.joint + ".position-cmd"
            minimumValue: minSpin.value
            maximumValue: maxSpin.value
        }
        HalGauge {
            Layout.fillWidth: true
            name: "joint" + root.joint + ".position-fb"
            fancy: false
            minimumValue: minSpin.value
            maximumValue: maxSpin.value
        }
    }
    ColumnLayout {
        Layout.fillWidth: false
        Layout.fillHeight: true
        HalSpinBox {
            id: minSpin
            Layout.fillWidth: true
            name: "joint" + root.joint + ".position-min"
            halPin.direction: HalPin.IO
            minimumValue: 0
            maximumValue: 100
        }
        HalSpinBox {
            id: maxSpin
            Layout.fillWidth: true
            name: "joint" + root.joint + ".position-max"
            halPin.direction: HalPin.IO
            minimumValue: 0
            maximumValue: 100
        }
        HalButton {
            Layout.fillHeight: true
            Layout.alignment: Layout.Center
            name: "joint" + root.joint + ".enable"
            checkable: true
            halPin.direction: HalPin.IO
            text: qsTr("Enable Joint: %1").arg(root.joint)
        }
    }
}
