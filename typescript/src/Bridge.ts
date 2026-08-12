export interface BridgeOptions {
    autoReconnect?: boolean;
    reconnectInterval?: number;
    maxRetries?: number;
}

export class PyJSBridge {
    private ws: any = null;
    private url: string;
    private callbacks: Map<string, { resolve: Function; reject: Function }> = new Map();
    private eventListeners: Map<string, Function[]> = new Map();
    private counter: number = 0;
    private options: Required<BridgeOptions>;
    private retryCount: number = 0;
    private isConnecting: boolean = false;
    public readonly version = "1.0.0-FINAL";

    constructor() {
        // Enforced IPv4 to match Python backbone loop exactly
        this.url = "ws://127.0.0.1:8765";
        this.options = {
            autoReconnect: true,
            reconnectInterval: 1000,
            maxRetries: 5,
        };
    }

    public on(event: string, callback: Function): void {
        if (!this.eventListeners.has(event)) this.eventListeners.set(event, []);
        this.eventListeners.get(event)!.push(callback);
    }

    private emit(event: string, data?: any): void {
        this.eventListeners.get(event)?.forEach(cb => cb(data));
    }

    /**
     * Connects to the Python server. Promise resolves ONLY when connection opens successfully.
     */
    public connect(): Promise<void> {
        if (this.isConnecting) return Promise.resolve();
        this.isConnecting = true;

        return new Promise((resolve, reject) => {
            try {
                this.ws = new WebSocket(this.url);

                this.ws.onopen = () => {
                    this.retryCount = 0;
                    this.isConnecting = false;
                    this.emit("open");
                    resolve(); // Safely unlock asynchronous calling capabilities
                };

                this.ws.onerror = (err: any) => {
                    this.emit("error", err);
                    this.isConnecting = false;
                    reject(new Error("Handshake aborted. Verify Python runtime is alive on 127.0.0.1:8765"));
                };

                this.ws.onmessage = (event: any) => {
                    const response = JSON.parse(event.data);
                    const callback = this.callbacks.get(response.id);
                    if (callback) {
                        if (response.error) callback.reject(new Error(response.error));
                        else callback.resolve(response.result);
                        this.callbacks.delete(response.id);
                    }
                };

                this.ws.onclose = () => {
                    this.isConnecting = false;
                    this.emit("close");
                    if (this.options.autoReconnect && this.retryCount < this.options.maxRetries) {
                        this.retryCount++;
                        setTimeout(() => this.connect(), this.options.reconnectInterval);
                    }
                };
            } catch (fatalError) {
                this.isConnecting = false;
                reject(fatalError);
            }
        });
    }

    public async call<T = any>(functionName: string, args: any[] = [], kwargs: object = {}): Promise<T> {
        if (!this.ws || this.ws.readyState !== 1) { // 1 means WebSocket.OPEN
            throw new Error(`Bridge pipeline is offline! Cannot execute: ${functionName}.`);
        }

        const id = `req_${++this.counter}_${Date.now()}`;
        const request = { id, function: functionName, args, kwargs };

        return new Promise<T>((resolve, reject) => {
            this.callbacks.set(id, { resolve, reject });
            this.ws!.send(JSON.stringify(request));
        });
    }
}
