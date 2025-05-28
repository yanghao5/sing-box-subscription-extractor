export interface Env {
	Proxy: KVNamespace
}

export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
	  const url = new URL(request.url);
	  if (url.pathname==='/whoami') {
		let value = request.headers.get('CF-Connecting-IP');
		return new Response(value, {
		  headers: { 'Content-Type': 'text/plain' }
		});
	  }
	  if (url.pathname === '/subscribe') {
		const token = url.searchParams.get('token');
		
		if (!token) {
		  return new Response('token is required', { status: 404 });
		}
		let subscriptionCorrespondingToToken = await env.Proxy.get(token);
		
		if (!subscriptionCorrespondingToToken) {
    		return new Response('invalid token', { status: 404 });
  		}else{
			const parseJSON=JSON.parse(subscriptionCorrespondingToToken)
			const responseJSON = JSON.stringify(parseJSON);
			console.log(responseJSON)
		  	return new Response(responseJSON, {
				headers: { 'Content-Type': 'application/json' }
		  	});
		}
	  }
	  return new Response('Not Found', { status: 404 });
	}
  } satisfies ExportedHandler<Env>;
