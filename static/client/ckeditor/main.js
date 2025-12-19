/**
 * This configuration was generated using the CKEditor 5 Builder. You can modify it anytime using this link:
 * https://ckeditor.com/ckeditor-5/builder/#installation/NodgNARATAdAnDADBSA2VAWVBGAzHOEADjl20UWyKIFZTEoaQQao4aM4HMUIBTAHYpEYYNjAjxUsNgC6kAIYKAJnADGy1BFlA===
 */
import {CLOUD_SERVICES_TOKEN_URL,LICENSE_KEY} from './creditial'


const {
	ClassicEditor,
	Autosave,
	Essentials,
	Paragraph,
	AutoLink,
	Bold,
	Italic,
	Link,
	CKBox,
	CloudServices,
	ImageBlock,
	ImageToolbar,
	ImageUpload,
	ImageInsert,
	ImageInsertViaUrl,
	AutoImage,
	PictureEditing,
	CKBoxImageEdit,
	ImageStyle,
	ImageResize,
	ImageInline,
	Alignment,
	Underline,
	GeneralHtmlSupport,
	Indent,
	IndentBlock,
	BlockToolbar
} = window.CKEDITOR;



const editorConfig = {
	toolbar: {
		items: [
			'undo',
			'redo',
			'|',
			'bold',
			'italic',
			'underline',
			'|',
			'link',
			'insertImage',
			'insertImageViaUrl',
			'ckbox',
			'|',
			'alignment',
			'|',
			'outdent',
			'indent'
		],
		shouldNotGroupWhenFull: false
	},
	plugins: [
		Alignment,
		AutoImage,
		AutoLink,
		Autosave,
		BlockToolbar,
		Bold,
		CKBox,
		CKBoxImageEdit,
		CloudServices,
		Essentials,
		GeneralHtmlSupport,
		ImageBlock,
		ImageInline,
		ImageInsert,
		ImageInsertViaUrl,
		ImageResize,
		ImageStyle,
		ImageToolbar,
		ImageUpload,
		Indent,
		IndentBlock,
		Italic,
		Link,
		Paragraph,
		PictureEditing,
		Underline
	],
	blockToolbar: ['bold', 'italic', '|', 'link', 'insertImage', '|', 'outdent', 'indent'],
	cloudServices: {
		tokenUrl: CLOUD_SERVICES_TOKEN_URL
	},
	htmlSupport: {
		allow: [
			{
				name: /^.*$/,
				styles: true,
				attributes: true,
				classes: true
			}
		]
	},
	image: {
		toolbar: ['imageStyle:inline', 'imageStyle:wrapText', 'imageStyle:breakText', '|', 'resizeImage', '|', 'ckboxImageEdit']
	},
	// initialData:'', // Removed to allow loading from DOM
	licenseKey: LICENSE_KEY,
	link: {
		addTargetToExternalLinks: true,
		defaultProtocol: 'https://',
		decorators: {
			toggleDownloadable: {
				mode: 'manual',
				label: 'Downloadable',
				attributes: {
					download: 'file'
				}
			}
		}
	},
	menuBar: {
		isVisible: true
	},
	// placeholder: 'Type or paste your content here!'
};

configUpdateAlert(editorConfig);

// ClassicEditor.create(document.querySelector('#editor'), editorConfig);
const sourceElement = document.querySelector('#editor');
if (sourceElement) {
	ClassicEditor.create(sourceElement, editorConfig)
		.then(editor => {
			// Make editor globally accessible
			window.editor = editor;

			// Sync CKEditor content to hidden input for Django
			editor.model.document.on('change:data', () => {
				const hiddenInput = document.getElementById('description');
				if (hiddenInput) {
					hiddenInput.value = editor.getData();
				}
			});

			// Initial Sync
			const hiddenInput = document.getElementById('description');
			if (hiddenInput) {
				hiddenInput.value = editor.getData();
			}
		})
		.catch(error => {
			console.error(error);
		});
}

/**
 * This function exists to remind you to update the config needed for premium features.
 * The function can be safely removed. Make sure to also remove call to this function when doing so.
 */
function configUpdateAlert(config) {
	if (configUpdateAlert.configUpdateAlertShown) {
		return;
	}

	const isModifiedByUser = (currentValue, forbiddenValue) => {
		if (currentValue === forbiddenValue) {
			return false;
		}

		if (currentValue === undefined) {
			return false;
		}

		return true;
	};

	const valuesToUpdate = [];

	configUpdateAlert.configUpdateAlertShown = true;

	if (!isModifiedByUser(config.licenseKey, '<YOUR_LICENSE_KEY>')) {
		valuesToUpdate.push('LICENSE_KEY');
	}

	if (!isModifiedByUser(config.cloudServices?.tokenUrl, '<YOUR_CLOUD_SERVICES_TOKEN_URL>')) {
		valuesToUpdate.push('CLOUD_SERVICES_TOKEN_URL');
	}

	if (valuesToUpdate.length) {
		window.alert(
			[
				'Please update the following values in your editor config',
				'to receive full access to Premium Features:',
				'',
				...valuesToUpdate.map(value => ` - ${value}`)
			].join('\n')
		);
	}
}
