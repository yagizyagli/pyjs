export interface BridgeOptions {
    autoReconnect?: boolean;
    reconnectInterval?: number;
    maxRetries?: number;
}

export class PyJSBridge {
    private ws: WebSocket | null = null;
    private url: string;
    private callbacks: Map<string, { resolve: Function; reject: Function }> = new Map();
    private eventListeners: Map<string, Function[]> = new Map();
    private counter: number = 0;
    private options: Required<BridgeOptions>;
    private retryCount: number = 0;
    public readonly version = "1.0.0-FINAL";

    constructor(host: string = "localhost", port: number = 8765, options?: BridgeOptions) {
        this.url = `ws://${host}:${port}`;
        this.options = {
            autoReconnect: options?.autoReconnect ?? true,
            reconnectInterval: options?.reconnectInterval ?? 2000,
            maxRetries: options?.maxRetries ?? 5,
        };
    }

    /**
     * Registers localized framework events (e.g., 'open', 'close', 'error')
     */
    public on(event: string, callback: Function): void {
        if (!this.eventListeners.has(event)) this.eventListeners.set(event, []);
        this.eventListeners.get(event)!.push(callback);
    }

    private emit(event: string, data?: any): void {
        this.eventListeners.get(event)?.forEach(cb => cb(data));
    }

    /**
     * Connects to the Python core engine with enterprise resiliency.
     */
    public connect(): Promise<void> {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                this.retryCount = 0;
                this.emit("open");
                resolve();
            };

            this.ws.onerror = (err) => {
                this.emit("error", err);
                reject(err);
            };

            this.ws.onmessage = (event) => {
                const response = JSON.parse(event.data);
                const callback = this.callbacks.get(response.id);
                if (callback) {
                    if (response.error) callback.reject(new Error(response.error));
                    else callback.resolve(response.result);
                    this.callbacks.delete(response.id);
                }
            };

            this.ws.onclose = () => {
                this.emit("close");
                if (this.options.autoReconnect && this.retryCount < this.options.maxRetries) {
                    this.retryCount++;
                    setTimeout(() => this.connect(), this.options.reconnectInterval);
                }
            };
        });
    }

    /**
     * Executes a native Python function and safely tracks asynchronous execution loops.
     */
    public async call<T = any>(functionName: string, args: any[] = [], kwargs: object = {}): Promise<T> {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            throw new Error("Bridge communication pipelines are currently decoupled.");
        }

        const id = `req_${++this.counter}_${Date.now()}`;
        const request = { id, function: functionName, args, kwargs };

        return new Promise<T>((resolve, reject) => {
            this.callbacks.set(id, { resolve, reject });
            this.ws!.send(JSON.stringify(request));
        });
    }
}
