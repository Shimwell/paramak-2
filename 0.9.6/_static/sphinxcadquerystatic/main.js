if ( WEBGL.isWebGLAvailable() === false ) {

    document.body.appendChild( WEBGL.getWebGLErrorMessage() );

}

var scenes = [], views, canvas, renderer;
var render_queued_flag = false;

window.addEventListener('load', init, false);
window.addEventListener('scroll', queueRender, false);
window.addEventListener('resize', queueRender, false);

function queueRender() {

    if ( !render_queued_flag ) {

        render_queued_flag = true;
        requestAnimationFrame( render );

    }

}

function load_amf_into_scene( scene ) {

    return function ( amfobject ) {

        scene.add( amfobject );
        queueRender();

    }

}

function load_geometry_into_scene( scene ) {

    return function ( geometry ) {

        var material = new THREE.MeshPhongMaterial( {

            color: scene.userData.view.color,
            specular: 0x111111,
            shininess: 20,

        } );
        geometry.computeVertexNormals();
        var mesh = new THREE.Mesh( geometry, material );
        scene.add( mesh );

        var edges = new THREE.EdgesGeometry( geometry, 15 );
        var line = new THREE.LineSegments( edges, new THREE.LineBasicMaterial( { color: 0x666666 } ) );
        scene.add( line );

        camera = scene.userData.camera;
        geometry.computeBoundingSphere();
        var distance = geometry.boundingSphere.radius / Math.atan( (camera.fov / 2) * (Math.PI / 180) );
        var factor = distance / Math.sqrt(2);
        camera.position.set( -factor / 3, -factor, factor );
        camera.lookAt( geometry.boundingSphere.center );
        scene.userData.controls.target = geometry.boundingSphere.center;
        scene.userData.distance_factor = factor;

        queueRender();

    }

}

function TranslucentGrid( size, divisions, color1, color2, opacity ) {

    size = size || 10;
    divisions = divisions || 10;
    color1 = new THREE.Color( color1 !== undefined ? color1 : 0x444444 );
    color2 = new THREE.Color( color2 !== undefined ? color2 : 0x888888 );

    var center = divisions / 2;
    var step = size / divisions;
    var halfSize = size / 2;

    var vertices = [], colors = [];

    for ( var i = 0, j = 0, k = - halfSize; i <= divisions; i ++, k += step ) {

        vertices.push( - halfSize, 0, k, halfSize, 0, k );
        vertices.push( k, 0, - halfSize, k, 0, halfSize );

        var color = i === center ? color1 : color2;

        color.toArray( colors, j ); j += 3;
        color.toArray( colors, j ); j += 3;
        color.toArray( colors, j ); j += 3;
        color.toArray( colors, j ); j += 3;

    }

    var geometry = new THREE.BufferGeometry();
    geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( vertices, 3 ) );
    geometry.addAttribute( 'color', new THREE.Float32BufferAttribute( colors, 3 ) );

    var material = new THREE.LineBasicMaterial( { vertexColors: THREE.VertexColors, opacity: opacity } );

    THREE.LineSegments.call( this, geometry, material );

}

TranslucentGrid.prototype = Object.create( THREE.LineSegments.prototype );
TranslucentGrid.prototype.constructor = TranslucentGrid;

function init() {

    var canvasElement = document.createElement('canvas');
    canvasElement.id = 'sphinxcadquerycanvas';
    document.body.appendChild(canvasElement);

    canvas = document.getElementById( 'sphinxcadquerycanvas' );

    renderer = new THREE.WebGLRenderer( {
        canvas: canvas,
        antialias: true,
        alpha: true,
        premultipliedAlpha: false,
    } );
    renderer.setPixelRatio( window.devicePixelRatio );

    views = document.querySelectorAll( '.sphinxcadqueryview' );

    for ( var n = 0; n < views.length; n ++ ) {

        var scene = new THREE.Scene();
        scene.background = new THREE.Color( 0xffffff );

        scene.userData.view = views[ n ];

        scene.add( new THREE.AmbientLight( 0x888888 ) );

        hemiLight = new THREE.HemisphereLight( 0x888888, 0x222222, 0.3 );
        hemiLight.position.set( 50, 50, 100 );
        scene.add( hemiLight );

        var gsize = parseFloat(scene.userData.view.gridsize);
        var gdivs = parseInt(scene.userData.view.griddivisions);
        var grid = new TranslucentGrid( gsize, gdivs, 0x888888, 0xdddddd, 0.6, );

        grid.rotateOnAxis( new THREE.Vector3( 1, 0, 0 ), 90 * ( Math.PI / 180 ) );
        grid.material.transparent = true;
        scene.add( grid );

        var camera = new THREE.PerspectiveCamera( 30, 1, 1, 10000 );
        camera.up.set( 0, 0, 1 );
        camera.position.set( 0, - 9, 6 );
        camera.add( new THREE.PointLight( 0xffffff, 0.5 ) );
        scene.add( camera );
        scene.userData.camera = camera;

        var controls = new THREE.OrbitControls( camera, views[ n ] );
        controls.addEventListener( 'change', queueRender );
        scene.userData.controls = controls;

        var loader = new THREE.LegacyJSONLoader();
        loader.load( scene.userData.view.fname, load_geometry_into_scene( scene ) );

        scenes.push( scene );

    }

    queueRender();

}

function updateSize() {

    var width = canvas.clientWidth;
    var height = canvas.clientHeight;

    if ( canvas.width !== width || canvas.height !== height ) {

        renderer.setSize( width, height, false );

    }

}

function render() {

    render_queued_flag = false;

    if ( canvas == undefined ) {

        queueRender();
        return;

    }

    updateSize();

    renderer.setScissorTest( true );

    const transform = `translateY(${window.scrollY}px)`;
    renderer.domElement.style.transform = transform;

    scenes.forEach( function ( scene ) {

        var rect = scene.userData.view.getBoundingClientRect();

        // set the viewport
        var width = rect.right - rect.left;
        var height = rect.bottom - rect.top;
        var left = rect.left;
        var bottom = renderer.domElement.clientHeight - rect.bottom;

        renderer.setViewport( left, bottom, width, height );
        renderer.setScissor( left, bottom, width, height );

        var camera = scene.userData.camera
        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        renderer.render( scene, scene.userData.camera );

    } );

}
