import { app } from '../../../scripts/app.js'
import { api } from '../../../scripts/api.js'

function chainCallback(object, property, callback) {
    if (object == undefined) {
        //This should not happen.
        console.error("Tried to add callback to non-existant object")
        return
    }
    if (property in object) {
        const callback_orig = object[property]
        object[property] = function () {
            const r = callback_orig.apply(this, arguments)
            callback.apply(this, arguments)
            return r
        }
    } else {
        object[property] = callback
    }
}

function fitHeight(node) {
    node.setSize([node.size[0], node.computeSize([node.size[0], node.size[1]])[1]])
    node?.graph?.setDirtyCanvas(true)
}

function addVideoPreview(nodeType) {
    chainCallback(nodeType.prototype, "onNodeCreated", function () {
        var element = document.createElement("div")
        const previewNode = this
        var previewWidget = this.addDOMWidget("videopreview", "preview", element, {
            serialize: false,
            hideOnZoom: false,
            getValue() {
                return element.value
            },
            setValue(v) {
                element.value = v
            },
        })
        previewWidget.computeSize = function (width) {
            if (this.aspectRatio && !this.parentEl.hidden) {
                let height = (previewNode.size[0] - 20) / this.aspectRatio + 10
                if (!(height > 0)) {
                    height = 0
                }
                this.computedHeight = height + 10
                return [width, height]
            }
            return [width, -4]//no loaded src, widget should not display
        }
        element.style['pointer-events'] = "none"
        previewWidget.value = { hidden: false, paused: false, params: {} }
        previewWidget.parentEl = document.createElement("div")
        previewWidget.parentEl.className = "vhs_preview"
        previewWidget.parentEl.style['width'] = "100%"
        element.appendChild(previewWidget.parentEl)
        previewWidget.videoEl = document.createElement("video")
        previewWidget.videoEl.controls = false
        previewWidget.videoEl.loop = true
        previewWidget.videoEl.muted = true
        previewWidget.videoEl.style['width'] = "100%"
        previewWidget.videoEl.addEventListener("loadedmetadata", () => {
            previewWidget.aspectRatio = previewWidget.videoEl.videoWidth / previewWidget.videoEl.videoHeight
            fitHeight(this)
        })
        previewWidget.videoEl.addEventListener("error", () => {
            //TODO: consider a way to properly notify the user why a preview isn't shown.
            previewWidget.parentEl.hidden = true
            fitHeight(this)
        })

        previewWidget.imgEl = document.createElement("img")
        previewWidget.imgEl.style['width'] = "100%"
        previewWidget.imgEl.hidden = true
        previewWidget.imgEl.onload = () => {
            previewWidget.aspectRatio = previewWidget.imgEl.naturalWidth / previewWidget.imgEl.naturalHeight
            fitHeight(this)
        }

        var timeout = null
        this.updateParameters = (params, force_update) => {
            if (!previewWidget.value.params) {
                if (typeof (previewWidget.value != 'object')) {
                    previewWidget.value = { hidden: false, paused: false }
                }
                previewWidget.value.params = {}
            }
            Object.assign(previewWidget.value.params, params)
            if (!force_update &&
                !app.ui.settings.getSettingValue("VHS.AdvancedPreviews", false)) {
                return
            }
            if (timeout) {
                clearTimeout(timeout)
            }
            if (force_update) {
                previewWidget.updateSource()
            } else {
                timeout = setTimeout(() => previewWidget.updateSource(), 100)
            }
        }
        previewWidget.updateSource = function () {
            if (this.value.params == undefined) {
                return
            }
            let params = {}
            Object.assign(params, this.value.params)//shallow copy
            this.parentEl.hidden = this.value.hidden
            if (
                params.format?.split('/')[0] == 'video' ||
                params.format == 'folder'
            ) {
                this.videoEl.autoplay = !this.value.paused && !this.value.hidden
                previewWidget.videoEl.src = api.apiURL('/view?' + new URLSearchParams(params))
                this.videoEl.hidden = false
                this.imgEl.hidden = true
            } else if (params.format?.split('/')[0] == 'image') {
                //Is animated image
                this.imgEl.src = api.apiURL('/view?' + new URLSearchParams(params))
                this.videoEl.hidden = true
                this.imgEl.hidden = false
            }
        }
        previewWidget.parentEl.appendChild(previewWidget.videoEl)
        previewWidget.parentEl.appendChild(previewWidget.imgEl)
    })
}

app.registerExtension({
    name: "TranscriptionTools.core",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData?.name == "TT-LoadVideoAudio") {
            chainCallback(nodeType.prototype, "onNodeCreated", function () {
                const pathWidget = this.widgets.find((w) => w.name === "video")
                chainCallback(pathWidget, "callback", (value) => {
                    if (!value) {
                        return
                    }
                    let parts = ["input", value]
                    let extension_index = parts[1].lastIndexOf(".")
                    let extension = parts[1].slice(extension_index + 1)
                    let format = "video"
                    if (["gif", "webp", "avif"].includes(extension)) {
                        format = "image"
                    }
                    format += "/" + extension
                    let params = { filename: parts[1], type: parts[0], format: format }
                    this.updateParameters(params, true)
                })
            })
            addVideoPreview(nodeType)
        }
    },
})
