namespace ChatLoaderAPI.Data_Access;

public class RequestRow
{
    public string url { get; set; }
    public DateTime request_time { get; set; }

    public RequestRow(string url, DateTime requestTime)
    {
        this.url = url;
        request_time = requestTime;
    }
}