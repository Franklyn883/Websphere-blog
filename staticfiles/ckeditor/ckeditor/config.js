/**
 * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	config.uiColor = '#192734';


    config.stylesSet =[
        {
            name: 'Custom Background color',
            element:'*',
            styles:{
                'background-color':'black'
            }
        }
    ]
};
