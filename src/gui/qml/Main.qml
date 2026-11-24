import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    property color ink: "#f6e8c8"
    property color mutedInk: "#b9a98b"
    property color night: "#11101d"
    property color panel: "#1d1728"
    property color panelRaised: "#2a1d32"
    property color edge: "#594052"
    property color crimson: "#b52f4b"
    property color crimsonBright: "#d94b62"
    property color gold: "#c5a35a"
    property color success: "#7fbf9b"
    property int pendingUnrenOption: 0
    function requestUnren(option) {
        pendingUnrenOption = option
        unrenConfirmDialog.open()
    }
    component GlossaryEditor: ColumnLayout {
        property string contextName: "global"
        property var entries: []
        Text { text: contextName === "menu" ? "Termos específicos dos menus" : "Termos gerais de tradução"; color: mutedInk }
        RowLayout { Layout.fillWidth: true
            TextField { id: originalField; placeholderText: "Original"; Layout.fillWidth: true }
            TextField { id: translationField; placeholderText: "Tradução preferida"; Layout.fillWidth: true }
            AppButton { text: "Adicionar"; onClicked: { appBackend.addGlossaryTerm(originalField.text, translationField.text, contextName); originalField.clear(); translationField.clear() } }
        }
        ListView { Layout.fillWidth: true; Layout.fillHeight: true; clip: true; model: entries
            delegate: RowLayout { width: parent.width; height: 36; Label { text: modelData; color: "#dae2fd"; Layout.fillWidth: true } AppButton { text: "Remover"; onClicked: appBackend.removeGlossaryTerm(modelData, contextName) } }
        }
    }
    component AppButton: Button {
        property string iconName: ""
        property string tooltipText: ""
        hoverEnabled: true
        ToolTip.visible: hovered
        ToolTip.text: tooltipText.length > 0 ? tooltipText : text
        ToolTip.delay: 450
        contentItem: RowLayout {
            spacing: iconName.length > 0 ? 8 : 0
            TablerIcon {
                name: iconName
                visible: iconName.length > 0
                size: 16
                Layout.alignment: Qt.AlignVCenter
            }
            Text {
                text: parent.parent.text
                color: parent.parent.enabled ? (parent.parent.hovered ? ink : "#c2aeb0") : "#665566"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }
        background: Rectangle {
            radius: 4
            color: !parent.enabled ? "#211827" : (parent.pressed ? "#7f243d" : (parent.hovered ? "#3a263d" : panelRaised))
            border.width: parent.activeFocus ? 2 : 1
            border.color: parent.activeFocus ? gold : (parent.hovered ? crimsonBright : edge)
        }
    }
    visible: true
    width: 1280
    height: 800
    minimumWidth: 960
    minimumHeight: 640
    title: "Alice"
    color: night

    header: ToolBar {
        background: Rectangle { color: "#191523" }
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            Rectangle { width: 3; height: 28; color: crimson; radius: 2 }
            Label { text: "Alice"; color: ink; font.pixelSize: 20; font.bold: true }
            Label { text: "TRADUÇÃO REN'PY  •  TEA & TINTA"; color: gold; font.pixelSize: 10 }
            Item { Layout.fillWidth: true }
            Label { text: "● LibreTranslate"; color: success }
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 240
            color: "#171321"
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 6
                Label { text: "THE RABBIT HOLE"; color: gold; font.pixelSize: 10; font.bold: true }
                AppButton { iconName: "layout-dashboard"; text: "Visão geral"; Layout.fillWidth: true; highlighted: true }
                AppButton { iconName: "folder"; text: "Projeto"; Layout.fillWidth: true; onClicked: projectDialog.open() }
                AppButton { iconName: "arrows-exchange"; text: "Tradução"; Layout.fillWidth: true; onClicked: translationDialog.open() }
                AppButton { iconName: "settings"; text: "Ferramentas"; Layout.fillWidth: true; onClicked: toolsDialog.open() }
                AppButton { iconName: "checklist"; text: "Revisão"; Layout.fillWidth: true; onClicked: reviewDialog.open() }
                AppButton { iconName: "files"; text: "Arquivos gerados"; Layout.fillWidth: true; onClicked: filesDialog.open() }
                AppButton { iconName: "book"; text: "Glossário"; Layout.fillWidth: true; onClicked: glossaryDialog.open() }
                AppButton { iconName: "activity"; text: "Diagnóstico"; Layout.fillWidth: true; onClicked: diagnosticDialog.open() }
                AppButton { iconName: "history"; text: "Histórico"; Layout.fillWidth: true; onClicked: historyDialog.open() }
                AppButton { iconName: "help-circle"; text: "Ajuda"; Layout.fillWidth: true; onClicked: helpDialog.open() }
                AppButton { iconName: "report"; text: "Relatório"; Layout.fillWidth: true; onClicked: reportDialog.open() }
                Item { Layout.fillHeight: true }
                AppButton { iconName: "settings"; text: "Configurações"; Layout.fillWidth: true; onClicked: settingsDialog.open() }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            anchors.margins: 28
            spacing: 20

            RowLayout {
                Layout.fillWidth: true
                ColumnLayout { Layout.fillWidth: true; Label { text: "Visão geral"; color: ink; font.pixelSize: 28; font.bold: true } Label { text: appBackend.status; color: mutedInk } }
                AppButton { iconName: "search"; tooltipText: "Escolher a pasta do jogo"; text: "Selecionar projeto"; onClicked: picker.open() }
                AppButton { iconName: "player-play"; text: "Iniciar tradução"; highlighted: true; enabled: appBackend.status === "Projeto válido" && !appBackend.translating && !appBackend.unrenRunning; onClicked: appBackend.startTranslation() }
                AppButton { iconName: "player-stop"; text: "Cancelar tradução"; enabled: appBackend.translating; onClicked: appBackend.cancelTranslation() }
            }

            RowLayout {
                Layout.fillWidth: true
                TextField {
                    id: projectPath
                    Layout.fillWidth: true
                    placeholderText: "Caminho do projeto (pasta que contém game)"
                    color: "#dae2fd"
                    placeholderTextColor: "#64748b"
                    background: Rectangle {
                        color: panel
                        radius: 4
                        border.width: activeFocus ? 2 : 1
                        border.color: activeFocus ? gold : (appBackend.status === "Projeto inválido" ? crimsonBright : edge)
                    }
                    Component.onCompleted: text = appBackend.project
                }
                Button { text: "Carregar"; enabled: !appBackend.unrenRunning; onClicked: appBackend.selectProject(projectPath.text) }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 86
                color: panel
                border.color: edge
                radius: 6
                RowLayout { anchors.fill: parent; anchors.margins: 18; Label { text: "PROJETO"; color: "#64748b"; font.pixelSize: 11 } Label { text: appBackend.project || "Nenhum projeto selecionado"; color: "#dae2fd"; Layout.fillWidth: true; elide: Text.ElideMiddle } }
            }

            RowLayout {
                Layout.fillWidth: true
                Repeater { model: [{label: "ARQUIVOS RPY", value: appBackend.files}, {label: "ENTRADAS", value: appBackend.entries}, {label: "STATUS", value: appBackend.status}]
                    delegate: Rectangle { Layout.fillWidth: true; height: 110; color: panelRaised; border.color: edge; radius: 6; Column { anchors.margins: 16; anchors.fill: parent; spacing: 10; Label { text: modelData.label; color: gold; font.pixelSize: 11 } Label { text: modelData.value; color: ink; font.pixelSize: modelData.label === "STATUS" ? 15 : 28; font.bold: true; elide: Text.ElideRight } } }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 58
                color: panel
                border.color: "#334155"
                radius: 5
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 10
                    RowLayout { Layout.fillWidth: true; Label { text: "PROGRESSO DA TRADUÇÃO"; color: "#94a3b8"; font.pixelSize: 11; font.bold: true } Item { Layout.fillWidth: true } Label { text: appBackend.progress + "%"; color: appBackend.progress === 100 ? "#4edea3" : "#adc6ff" } }
                    Rectangle { Layout.fillWidth: true; height: 10; color: night; radius: 5; border.color: edge; Rectangle { width: parent.width * appBackend.progress / 100; height: parent.height; color: appBackend.progress === 100 ? success : crimson; radius: 5 } }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 74
                color: panelRaised
                border.color: edge
                radius: 6
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 12
                    Label { text: "QUALIDADE DA TRADUÇÃO"; color: gold; font.pixelSize: 10; font.bold: true }
                    Repeater {
                        model: appBackend.qualitySummary
                        delegate: Label {
                            text: modelData
                            color: modelData.indexOf("problemas") >= 0 ? "#e5a56b" : ink
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 112
                Layout.minimumHeight: 112
                color: panel
                border.color: "#334155"
                radius: 6
                visible: appBackend.filesGenerated.length > 0
                ColumnLayout { anchors.fill: parent; anchors.margins: 14; Label { text: "ARQUIVOS GERADOS"; color: "#94a3b8"; font.pixelSize: 11; font.bold: true } Label { id: generatedText; text: appBackend.filesGenerated; color: "#4edea3"; font.family: "Consolas"; wrapMode: Text.WrapAnywhere; Layout.fillWidth: true; Layout.fillHeight: true; clip: true } }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 320
                Layout.minimumHeight: 240
                color: "#090d16"
                border.color: "#334155"
                radius: 6
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 14
                    Label { text: "LOGS E DIAGNÓSTICOS"; color: "#94a3b8"; font.pixelSize: 11; font.bold: true }
                    ScrollView {
                        id: logScroll
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        TextArea {
                            id: logArea
                            readOnly: true
                            text: appBackend.logs
                            color: "#94a3b8"
                            font.family: "Consolas"
                            font.pixelSize: 12
                            wrapMode: TextArea.Wrap
                            background: Rectangle { color: "transparent" }
                            onTextChanged: Qt.callLater(function() {
                                logArea.cursorPosition = logArea.length
                                logScroll.contentItem.contentY = Math.max(0, logScroll.contentItem.contentHeight - logScroll.height)
                            })
                        }
                    }
                }
            }
            Item { Layout.fillHeight: true }
        }
    }

    FolderDialog {
        id: picker
        title: "Selecione a pasta do projeto"
        onAccepted: {
            projectPath.text = selectedFolder.toString().replace("file:///", "")
            appBackend.selectProject(projectPath.text)
        }
    }

    Dialog {
        id: settingsDialog
        title: "Configurações de tradução"
        modal: true
        width: 440
        standardButtons: Dialog.Save | Dialog.Cancel
        onAccepted: appBackend.saveSettings(sourceBox.currentText, targetBox.currentText, engineBox.currentText, Number(batchBox.currentText), endpointBox.text, Number(timeoutBox.text), Number(retriesBox.text))

        contentItem: ColumnLayout {
            implicitWidth: 380
            spacing: 12
            Label { text: "Idioma de origem"; color: "#dae2fd" }
            ComboBox { id: sourceBox; Layout.fillWidth: true; model: ["en", "es", "fr", "de", "ja"] }
            Label { text: "Idioma de destino"; color: "#dae2fd" }
            ComboBox { id: targetBox; Layout.fillWidth: true; model: ["pt-BR", "pt", "es", "fr", "de"] }
            Label { text: "Motor de tradução"; color: "#dae2fd" }
            ComboBox { id: engineBox; Layout.fillWidth: true; model: ["libretranslate"] }
            Label { text: "Tamanho do lote"; color: "#dae2fd" }
            ComboBox { id: batchBox; Layout.fillWidth: true; model: ["50", "100", "200", "500"]; currentIndex: 2 }
            Label { text: "Endpoint de tradução"; color: "#dae2fd" }
            TextField { id: endpointBox; Layout.fillWidth: true; text: appBackend.apiUrl }
            Label { text: "Timeout (segundos)"; color: "#dae2fd" }
            TextField { id: timeoutBox; Layout.fillWidth: true; text: String(appBackend.timeout); validator: IntValidator { bottom: 1 } }
            Label { text: "Tentativas"; color: "#dae2fd" }
            TextField { id: retriesBox; Layout.fillWidth: true; text: String(appBackend.maxRetries); validator: IntValidator { bottom: 0 } }
        }
    }

    Dialog {
        id: projectDialog
        title: "Projeto Ren'Py"
        modal: true
        width: 560
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            implicitWidth: 520
            spacing: 12
            Label { text: "Caminho"; color: "#64748b" }
            TextField { text: appBackend.project || "Nenhum projeto selecionado"; readOnly: true; Layout.fillWidth: true }
            Label { text: "Status: " + appBackend.status; color: appBackend.status === "Projeto válido" ? "#4edea3" : "#ffb95f" }
            Label { text: "Arquivos .rpy encontrados: " + appBackend.files; color: "#dae2fd" }
            AppButton { iconName: "checklist"; text: "Validar estrutura do projeto"; Layout.fillWidth: true; onClicked: appBackend.validateProject() }
            AppButton { iconName: "player-play"; text: "Simular tradução"; Layout.fillWidth: true; onClicked: appBackend.simulateTranslation() }
            AppButton { iconName: "language"; text: "Adicionar Português ao menu"; Layout.fillWidth: true; onClicked: appBackend.addPortugueseLanguageOption() }
        }
    }

    Dialog {
        id: translationDialog
        title: "Configuração e execução"
        modal: true
        width: 560
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            implicitWidth: 520
            spacing: 12
            Label { text: "Origem: " + appBackend.sourceLanguage; color: "#dae2fd" }
            Label { text: "Destino: " + appBackend.targetLanguage; color: "#dae2fd" }
            Label { text: "Motor: " + appBackend.engine; color: "#dae2fd" }
            ProgressBar { Layout.fillWidth: true; value: appBackend.progress; from: 0; to: 100 }
            Label { text: appBackend.status; color: "#94a3b8" }
            AppButton { iconName: "player-play"; text: "Iniciar tradução"; Layout.fillWidth: true; highlighted: true; enabled: appBackend.status === "Projeto válido" && !appBackend.translating && !appBackend.unrenRunning; onClicked: { appBackend.startTranslation(); translationDialog.close() } }
            AppButton { iconName: "player-stop"; text: "Cancelar tradução"; Layout.fillWidth: true; enabled: appBackend.translating; onClicked: appBackend.cancelTranslation() }
        }
    }

    Dialog {
        id: toolsDialog
        title: "Ferramentas"
        modal: true
        width: 680
        height: 500
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            spacing: 14
            Label {
                text: "Ferramentas do projeto"
                color: ink
                font.pixelSize: 20
                font.bold: true
                Layout.fillWidth: true
            }
            Label {
                text: "Utilitários para preparar, inspecionar e manter o jogo Ren'Py."
                color: mutedInk
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }
            Rectangle {
                Layout.fillWidth: true
                color: panel
                border.color: edge
                radius: 6
                implicitHeight: 150
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 8
                    RowLayout {
                        Layout.fillWidth: true
                        TablerIcon { name: "archive"; size: 24 }
                        Label { text: "UnRen"; color: ink; font.pixelSize: 18; font.bold: true; Layout.fillWidth: true }
                        Label { text: "Ferramenta de preparação"; color: gold }
                    }
                    Label {
                        text: "Extrai arquivos .rpa, descompila .rpyc/.rpymc e ativa opções auxiliares de desenvolvimento. Um backup é criado antes da execução."
                        color: mutedInk
                        wrapMode: Text.Wrap
                        Layout.fillWidth: true
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        AppButton {
                            iconName: "player-play"
                            text: "Abrir UnRen"
                            highlighted: true
                            enabled: !appBackend.unrenRunning
                            onClicked: { appBackend.inspectUnren(); unrenDialog.open() }
                        }
                    }
                }
            }
            Item { Layout.fillHeight: true }
        }
    }

    Dialog {
        id: unrenDialog
        title: "Ferramentas > UnRen"
        modal: true
        width: 580
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            implicitWidth: 540
            spacing: 12
            Label {
                text: "O modo assistido extrai .rpa e descompila .rpyc/.rpymc. Um backup dos arquivos .rpy, .rpa e compilados será criado antes da execução."
                color: mutedInk
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }
            Label { text: appBackend.unrenSummary; color: ink; wrapMode: Text.Wrap; Layout.fillWidth: true }
            Label {
                text: "Status: " + appBackend.unrenStatus
                color: appBackend.unrenRunning ? gold
                    : appBackend.unrenStatus.indexOf("cancelado") >= 0 ? crimsonBright
                    : appBackend.unrenStatus.indexOf("concluído") >= 0 ? success
                    : mutedInk
                font.bold: true
                Layout.fillWidth: true
            }
            Label {
                text: "Ações disponíveis"
                color: mutedInk
                Layout.fillWidth: true
            }
            GridLayout {
                columns: 2
                Layout.fillWidth: true
                AppButton {
                    iconName: "archive"
                    text: "1. Extrair RPA"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(1)
                }
                AppButton {
                    iconName: "file-text"
                    text: "2. Descompilar RPYC"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(2)
                }
                AppButton {
                    iconName: "settings"
                    text: "3. Console e desenvolvedor"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(3)
                }
                AppButton {
                    iconName: "history"
                    text: "4. Quick Save/Load"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(4)
                }
                AppButton {
                    iconName: "player-play"
                    text: "5. Pular conteúdo não visto"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(5)
                }
                AppButton {
                    iconName: "arrows-exchange"
                    text: "6. Ativar rollback"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(6)
                }
                AppButton {
                    iconName: "checklist"
                    text: "7. Executar opções 3-6"
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(7)
                }
                AppButton {
                    iconName: "player-play"
                    text: "8. Executar opções 1-6"
                    highlighted: true
                    enabled: !appBackend.unrenRunning
                    Layout.fillWidth: true
                    onClicked: requestUnren(8)
                }
            }
            AppButton {
                iconName: "player-stop"
                text: "Cancelar UnRen"
                enabled: appBackend.unrenRunning
                Layout.fillWidth: true
                onClicked: appBackend.cancelUnren()
            }
        }
    }

    Dialog {
        id: unrenConfirmDialog
        title: "Confirmar execução do UnRen"
        modal: true
        standardButtons: Dialog.Cancel
        contentItem: ColumnLayout {
            implicitWidth: 500
            spacing: 10
            Label {
                text: "Esta ação pode alterar arquivos do jogo. A Alice criará um backup antes de executar a opção " + pendingUnrenOption + ". Deseja continuar?"
                color: ink
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }
            Label {
                text: "A execução será cancelada automaticamente após 10 minutos."
                color: mutedInk
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }
            AppButton {
                iconName: "player-play"
                text: "Confirmar e executar"
                highlighted: true
                Layout.fillWidth: true
                onClicked: {
                    if (appBackend.runUnrenOption(pendingUnrenOption)) {
                        unrenConfirmDialog.close()
                    }
                }
            }
        }
    }

    Dialog {
        id: filesDialog
        title: "Arquivos gerados"
        modal: true
        standardButtons: Dialog.Close
        width: 700
        height: 460
        contentItem: ColumnLayout {
            spacing: 10
            Label { text: "Arquivos produzidos pela última execução"; color: "#94a3b8" }
            TextArea { id: generatedFilesArea; Layout.fillWidth: true; Layout.fillHeight: true; readOnly: true; text: appBackend.filesGenerated || "Nenhum arquivo gerado ainda."; color: "#4edea3"; font.family: "Consolas"; wrapMode: TextArea.Wrap }
            AppButton { iconName: "folder"; text: "Abrir pasta de saída"; Layout.fillWidth: true; onClicked: appBackend.openOutputFolder() }
            AppButton { iconName: "copy"; text: "Copiar caminhos"; Layout.fillWidth: true; onClicked: appBackend.copyPath(generatedFilesArea.text) }
            AppButton { iconName: "file-text"; text: "Abrir primeiro arquivo"; Layout.fillWidth: true; enabled: appBackend.filesGenerated.length > 0; onClicked: appBackend.openGeneratedFile(appBackend.filesGenerated.split("\n")[0]) }
            AppButton { iconName: "archive"; text: "Criar backup dos arquivos"; Layout.fillWidth: true; onClicked: appBackend.backupGeneratedFiles() }
            AppButton { iconName: "restore"; text: "Restaurar último backup"; Layout.fillWidth: true; onClicked: appBackend.restoreLatestGeneratedBackup() }
        }
    }

    Dialog {
        id: glossaryDialog
        title: "Glossário"
        modal: true
        width: 620
        height: 560
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            spacing: 10
            TabBar { id: glossaryTabs; Layout.fillWidth: true; TabButton { text: "Global" } TabButton { text: "Menu" } }
            StackLayout { currentIndex: glossaryTabs.currentIndex; Layout.fillWidth: true; Layout.fillHeight: true
                ColumnLayout { GlossaryEditor { contextName: "global"; entries: appBackend.glossaryEntries } }
                ColumnLayout { GlossaryEditor { contextName: "menu"; entries: appBackend.menuGlossaryEntries } }
            }
            AppButton { text: "Salvar glossário"; Layout.fillWidth: true; highlighted: true; onClicked: appBackend.saveGlossary() }
            TextField { id: glossaryPath; Layout.fillWidth: true; placeholderText: "Caminho JSON para importar/exportar" }
            RowLayout {
                AppButton { text: "Importar"; onClicked: appBackend.importGlossary(glossaryPath.text, glossaryTabs.currentIndex === 1 ? "menu" : "global") }
                AppButton { text: "Exportar"; onClicked: appBackend.exportGlossary(glossaryPath.text, glossaryTabs.currentIndex === 1 ? "menu" : "global") }
            }
        }
    }

    Dialog {
        id: diagnosticDialog
        title: "Diagnóstico do LibreTranslate"
        modal: true
        width: 560
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            spacing: 12
            Label { text: "Endpoint"; color: "#94a3b8" }
            TextField { text: "http://localhost:5000/translate"; readOnly: true; Layout.fillWidth: true }
            Label { text: "Status: " + appBackend.connectionStatus; color: appBackend.connectionStatus === "Conectado" ? "#4edea3" : "#ffb95f" }
            AppButton { iconName: "activity"; text: "Testar conexão"; Layout.fillWidth: true; onClicked: appBackend.testConnection() }
            AppButton { iconName: "search"; text: "Verificar cache"; Layout.fillWidth: true; onClicked: appBackend.refreshDiagnostics() }
            AppButton { iconName: "trash"; text: "Limpar cache deste projeto"; Layout.fillWidth: true; onClicked: cacheConfirmDialog.open() }
            AppButton { iconName: "restore"; text: "Restaurar último backup"; Layout.fillWidth: true; onClicked: appBackend.restoreLatestCacheBackup() }
            AppButton { iconName: "folder"; text: "Abrir pasta do cache"; Layout.fillWidth: true; onClicked: appBackend.openCacheFolder() }
            Label { text: "Cache atual: " + appBackend.cachePath; color: "#64748b"; wrapMode: Text.Wrap; Layout.fillWidth: true }
            Label { text: appBackend.diagnosticSummary; color: "#dae2fd"; wrapMode: Text.Wrap; Layout.fillWidth: true }
            Label { text: "O teste consulta o endpoint /languages sem bloquear a interface."; color: "#64748b"; wrapMode: Text.Wrap; Layout.fillWidth: true }
        }
    }

    Dialog {
        id: historyDialog
        title: "Histórico de execuções"
        modal: true
        width: 820
        height: 500
        standardButtons: Dialog.Close
        contentItem: ColumnLayout {
            spacing: 10
            Label { text: "Últimas execuções da Alice"; color: "#94a3b8" }
            ListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: appBackend.historyEntries
                delegate: Label { width: ListView.view.width; height: 32; text: modelData; color: "#dae2fd"; font.family: "Consolas"; elide: Text.ElideMiddle }
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AlwaysOn }
            }

            Label { visible: appBackend.historyEntries.length === 0; text: "Nenhuma execução registrada."; color: "#64748b" }
        }
    }

    Dialog {
        id: helpDialog
        title: "Ajuda da Alice"
        modal: true
        width: 760
        height: 560
        standardButtons: Dialog.Close
        contentItem: ScrollView {
            TextArea {
                readOnly: true
                color: "#dae2fd"
                font.family: "Consolas"
                wrapMode: TextArea.Wrap
                text: "FLUXO RÁPIDO\n\n1. Selecione a pasta do jogo que contém game/.\n2. Confirme o status Projeto válido.\n3. Configure idiomas e tamanho do lote.\n4. Teste o LibreTranslate na tela Diagnóstico.\n5. Inicie a tradução e acompanhe os logs.\n6. Revise as entradas e salve alterações.\n7. Abra os arquivos gerados e selecione Português no jogo.\n\nESTRUTURA ESPERADA\n\nMeuJogo/\n  game/\n    script.rpy\n\nSAÍDA\n\nOs arquivos são gerados em game/tl/portuguese/. O cache do projeto fica em .alice/cache.json e o histórico em history.json.\n\nGLOSSÁRIO\n\nUse a aba Menu para termos específicos da interface. O glossário tem prioridade sobre o motor de tradução no contexto configurado.\n\nPROBLEMAS COMUNS\n\n- Se o jogo não mostrar Português, use Projeto > Adicionar Português ao menu.\n- Se uma frase não for traduzida, verifique a tela Revisão e o arquivo de origem.\n- Se o motor falhar, abra Diagnóstico e teste o endpoint configurado.\n- O cache pode ser validado, limpo e restaurado pela tela Diagnóstico."
            }
        }
    }

    Dialog {
        id: reportDialog
        title: "Relatório da execução"
        modal: true
        width: 820
        height: 600
        standardButtons: Dialog.Close
        contentItem: ScrollView {
            ColumnLayout {
                width: parent.width
                TextArea {
                    id: reportArea
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    readOnly: true
                    color: "#dae2fd"
                    font.family: "Consolas"
                    wrapMode: TextArea.Wrap
                    text: "ALICE - RELATÓRIO DE QUALIDADE\n\nProjeto:\n" + appBackend.project + "\n\nStatus:\n" + appBackend.status + "\n\nProgresso:\n" + appBackend.progress + "%\n\n" + appBackend.qualitySummary.join("\n") + "\n\nArquivos RPY:\n" + appBackend.files + "\n\nEntradas extraídas:\n" + appBackend.entries + "\n\nArquivos gerados:\n" + (appBackend.filesGenerated || "Nenhum arquivo gerado.") + "\n\nLOGS:\n" + appBackend.logs
                }
                RowLayout {
                    AppButton { text: "Exportar TXT"; onClicked: appBackend.exportReport("txt") }
                    AppButton { text: "Exportar JSON"; onClicked: appBackend.exportReport("json") }
                }
            }
        }
    }

    Dialog {
        id: reviewDialog
        title: "Revisão das traduções"
        modal: true
        standardButtons: Dialog.Close
        width: Math.min(parent.width - 80, 1050)
        height: Math.min(parent.height - 80, 650)
        property int selectedIndex: -1
        contentItem: ColumnLayout {
            spacing: 10
            RowLayout {
                Layout.fillWidth: true
                Label { text: appBackend.reviewEntries.length + " entrada(s) carregada(s)"; color: "#94a3b8"; Layout.fillWidth: true }
                ComboBox { id: reviewFilter; model: ["Todas", "Revisadas", "Pendentes", "Com problemas"] }
                TextField { id: reviewSearch; placeholderText: "Buscar texto..."; Layout.preferredWidth: 220 }
            }
            ListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                ScrollBar.vertical: ScrollBar {
                    policy: ScrollBar.AlwaysOn
                }
                model: {
                    var items = appBackend.reviewEntries
                    if (reviewFilter.currentIndex === 1)
                        items = items.filter(function(item) { return item.indexOf("[REVISADA]") === 0 })
                    else if (reviewFilter.currentIndex === 2)
                        items = items.filter(function(item) { return item.indexOf("[REVISADA]") !== 0 })
                    else if (reviewFilter.currentIndex === 3)
                        items = items.filter(function(item) {
                            var reviewIndex = appBackend.reviewIndexForDisplay(item)
                            return appBackend.reviewHasIssue(reviewIndex)
                        })
                    if (reviewSearch.text.length > 0)
                        items = items.filter(function(item) { return item.toLowerCase().indexOf(reviewSearch.text.toLowerCase()) >= 0 })
                    return items
                }
                delegate: Rectangle {
                    width: ListView.view.width
                    height: entryText.implicitHeight + 18
                    color: index % 2 ? panel : "#171321"
                    border.color: "#334155"
                    Text { id: entryText; anchors.fill: parent; anchors.margins: 9; text: modelData; color: "#dae2fd"; font.family: "Consolas"; font.pixelSize: 12; wrapMode: Text.Wrap }
                    MouseArea { anchors.fill: parent; onClicked: { reviewDialog.selectedIndex = appBackend.reviewIndexForDisplay(modelData); reviewEditor.text = appBackend.reviewTranslation(reviewDialog.selectedIndex) } }
                }
                Label { anchors.centerIn: parent; visible: appBackend.reviewEntries.length === 0; text: "Nenhuma entrada disponível. Execute uma tradução primeiro."; color: "#64748b" }
            }
            RowLayout {
                Label { text: reviewDialog.selectedIndex >= 0 ? ("Entrada " + (reviewDialog.selectedIndex + 1) + "/" + appBackend.reviewEntries.length) : "Selecione uma entrada para editar"; color: "#94a3b8"; Layout.fillWidth: true }
                AppButton { text: "Anterior"; enabled: reviewDialog.selectedIndex > 0; onClicked: { reviewDialog.selectedIndex = appBackend.previousReviewIndex(reviewDialog.selectedIndex); reviewEditor.text = appBackend.reviewTranslation(reviewDialog.selectedIndex) } }
                AppButton { text: "Próxima"; enabled: reviewDialog.selectedIndex >= 0 && reviewDialog.selectedIndex < appBackend.reviewEntries.length - 1; onClicked: { reviewDialog.selectedIndex = appBackend.nextReviewIndex(reviewDialog.selectedIndex); reviewEditor.text = appBackend.reviewTranslation(reviewDialog.selectedIndex) } }
            }
            Label { text: reviewDialog.selectedIndex >= 0 && appBackend.reviewIsSameAsOriginal(reviewDialog.selectedIndex) ? "A tradução é igual ao original" : ""; color: "#ffb95f" }
            TextArea { id: reviewEditor; Layout.fillWidth: true; implicitHeight: 80; enabled: reviewDialog.selectedIndex >= 0; placeholderText: "Tradução"; color: ink; background: Rectangle { color: panel; border.color: edge } }
            Button { text: "Salvar alteração"; enabled: reviewDialog.selectedIndex >= 0; onClicked: appBackend.updateReviewEntry(reviewDialog.selectedIndex, reviewEditor.text) }
            Button { text: "Salvar e regenerar arquivos"; enabled: appBackend.reviewEntries.length > 0; highlighted: true; onClicked: appBackend.saveReviewChanges() }
        }
    }

    Dialog {
        id: cacheConfirmDialog
        title: "Limpar cache"
        modal: true
        standardButtons: Dialog.Yes | Dialog.No
        contentItem: Label {
            text: "Todas as traduções armazenadas do projeto atual serão removidas. Um backup será criado. Deseja continuar?"
            color: "#dae2fd"
            wrapMode: Text.Wrap
            padding: 18
        }
        onAccepted: appBackend.clearProjectCache()
    }
}
