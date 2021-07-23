const whitelist = ["/bot"];
const tg_host = "api.telegram.org";
addEventListener('fetch', event =>{
	event.respondWith(handleRequest(event.request))
})
function validate(path) {
	for (var i = 0; i < whitelist.length; i++) {
		if (path.startsWith(whitelist[i])) return true;
	}
	return false;
}
async function handleRequest(request) {
	var u = new URL(request.url);
	u.host = tg_host;
	if (!validate(u.pathname)) return new Response('Unauthorized', {
		status: 403
	});
	var req = new Request(u, {
		method: request.method,
		headers: request.headers,
		body: request.body
	});
	const result = await fetch(req);
	return result;
}