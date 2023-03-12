using Dapper;
using Npgsql;

namespace ChatLoaderAPI.Data_Access;

public static class DbMethods
{
    private const string TableName = "public.requests";
    
    /// <summary>
    /// test commit
    /// </summary>
    /// <param name="request"></param>
    /// <param name="conn"></param>
    public static async Task Commit(RequestRow request, NpgsqlConnection conn)
    {
        var sqlQuery = $@"INSERT INTO {TableName} (url, request_time)
                               VALUES ('{request.url}', '{request.request_time}')";
        await conn.ExecuteAsync(sqlQuery);
    }

    public static async Task<int> CommitAndGetId(RequestRow request, NpgsqlConnection conn)
    {
        await Commit(request, conn);
        const string sqlQuery = $@"SELECT MAX(id) FROM {TableName}";
        return await conn.QuerySingleAsync<int>(sqlQuery);
    }

    public static async Task<string?> GetById(NpgsqlConnection conn, int requestId)
    {
        var sqlQuery = $@"SELECT answer FROM {TableName} WHERE id = {requestId}";
        return await conn.QuerySingleAsync<string?>(sqlQuery);
    }
}