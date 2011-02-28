<?
// vim: set expandtab tabstop=2 shiftwidth=2 autoindent smartindent:
function get_rtmp() {
  $proxyUrl = 'http://127.0.0.1/umsp/plugins/rtmp-proxy.php?'; //This path might change

  $app = PATH_TO_RTMP_APP; // probably IP.IP.IP.IP:PORT/onDemand/ or something. include the server and port
  $path = PATH_TOTHE_RTMP_FILE; //probably mp4:XXXXXXXXXXXX
  $format = 'flv'; // file format to transcode to. Most time.. flv to flv works good to fix framerate issue. Can't use Mp4 or similar (g3p)..
  $title = 'movieTitle'; //movie title... get it from your plugin... or juste use a default name
  $content_type = '"video/x-flv"'; //What content-type should be used in the header.. see $format

  $query = array(
    'r'               =>  urlencode($app),
    'y'               =>  urlencode($path),
    'format'       =>  urlencode($format),
    'title'          =>  urlencode($title),
    'content-type'   =>  urlencode($content_type),
  );

  $queryStr = http_build_query($query);
  $location = $proxyUrl . $queryStr;

  $mediaItem = array (
    'id'            => 'umsp://plugins/rtmp-null',
    'dc:title'      => $title,
    'res'           => $location,
    'upnp:class'    => 'object.item.videoitem',
    'protocolInfo'  => 'http-get:*:'.$content_type.':*',
  );

  return $mediaItem;
}

function get_rtve() {
  return array(
    'id'             => 'umsp://plugins/rtve',
    'parentID'       => '0',
    'dc:title'       => 'RTVE',
    'upnp:class'     => 'object.container',
    'upnp:album_art' => '',
  );
}
global $myMediaItems;

$myMediaItems[] = get_rtve();
$myMediaItems[] = get_rtmp();

//print_r($myMediaItems);
?>
