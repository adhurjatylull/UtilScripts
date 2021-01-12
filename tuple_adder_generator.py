from string import ascii_uppercase


def comma_string(n):
    return ', '.join(ascii_uppercase[i] for i in range(n))


def type_string(n):
    if n == 1:
        return 'A'
    return f'({comma_string(n)})'


def tuple_args(n, name='Value'):
    if n == 1:
        return name
    return ', '.join(f'{name}.Item{i+1}' for i in range(n))


template = lambda n: f'''
public class TupleAdder<{comma_string(n)}>
{{
    public {type_string(n)} Value {{ get; private set; }}

    public TupleAdder({type_string(n)} Value)
    {{
        this.Value = Value;
    }}

    public TupleAdder<{type_string(n+1)}> Add<{ascii_uppercase[n]}>({ascii_uppercase[n]} nextValue)
    {{
        return new TupleAdder<{type_string(n+1)}>(({tuple_args(n)}, nextValue));
    }}
}}
'''

def make_classes(n):
    return ''.join(template(i+1) for i in range(n))


extension_template = lambda n: f'''
public static Result<{type_string(n+1)}> TupleBind<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, Result<{ascii_uppercase[n]}>> f)
{{
    return x.Transform(y => f({tuple_args(n, "y")}).Transform(z => new TupleAdder<{comma_string(n)}>(y).Add(z).Value));
}}

public static Result<{type_string(n+1)}> TupleTransform<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, {ascii_uppercase[n]}> f)
{{
    return x.Transform(y => new TupleAdder<{comma_string(n)}>(y).Add(f({tuple_args(n, "y")})).Value);
}}

public static async Task<Result<{type_string(n+1)}>> TupleBind<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, Task<Result<{ascii_uppercase[n]}>>> f)
{{
    return await x.TransformAsync(async y => (await f({tuple_args(n, "y")})).Transform(z => new TupleAdder<{comma_string(n)}>(y).Add(z).Value));
}}

public static async Task<Result<{type_string(n+1)}>> TupleTransform<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, Task<{ascii_uppercase[n]}>> f)
{{
    return await x.TransformAsync(async y => new TupleAdder<{comma_string(n)}>(y).Add(await f({tuple_args(n, "y")})).Value);
}}
'''

existing_extension_template = lambda n: f'''
public static Result<{type_string(n+1)}> TupleBind<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{type_string(n)}, Result<{ascii_uppercase[n]}>> f)
{{
    return x.Transform(y => f(({tuple_args(n, "y")})).Transform(z => new TupleAdder<{comma_string(n)}>(y).Add(z).Value));
}}

public static Result<{type_string(n+1)}> TupleTransform<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{type_string(n)}, {ascii_uppercase[n]}> f)
{{
    return x.Transform(y => new TupleAdder<{comma_string(n)}>(y).Add(f(({tuple_args(n, "y")}))).Value);
}}

public static async Task<Result<{type_string(n+1)}>> TupleBind<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{type_string(n)}, Task<Result<{ascii_uppercase[n]}>>> f)
{{
    return await x.TransformAsync(async y => (await f(({tuple_args(n, "y")}))).Transform(z => new TupleAdder<{comma_string(n)}>(y).Add(z).Value));
}}

public static async Task<Result<{type_string(n+1)}>> TupleTransform<{comma_string(n+1)}>(this Result<{type_string(n)}> x, Func<{type_string(n)}, Task<{ascii_uppercase[n]}>> f)
{{
    return await x.TransformAsync(async y => new TupleAdder<{comma_string(n)}>(y).Add(await f(({tuple_args(n, "y")}))).Value);
}}

public static Result<TRes> OnSuccess<{comma_string(n)}, TRes>(this Result<{type_string(n)}> Result, Func<{comma_string(n)}, Result<TRes>> Func)
{{
    if (Result.Failure)
        return Result.To<TRes>();

    var val = Func({tuple_args(n, "Result.Value")});
    return Infrastructure.Result.Combine(Result, val).To(val.Value);
}}

public static Result OnSuccess<{comma_string(n)}>(this Result<{type_string(n)}> Result, Func<{comma_string(n)}, Result> Func)
{{
    if (Result.Failure)
        return Result;

    var val = Func({tuple_args(n, "Result.Value")});
    return Infrastructure.Result.Combine(Result, val);
}}

public static Result<{type_string(n)}> Tee<{comma_string(n)}>(this Result<{type_string(n)}> x, Action<{comma_string(n)}> f)
{{
    if (x.Success)
        f({tuple_args(n, "x.Value")});
    return x;
}}

public static Result<TSuccess> Transform<{comma_string(n)}, TSuccess>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, TSuccess> transform)
{{
    if(x.Failure)
        return x.To<TSuccess>();
    return new Try().Expect().Execute(() => Result.Ok(transform({tuple_args(n, "x.Value")})));
}}

public static async Task<Result<TRes>> OnSuccess<{comma_string(n)}, TRes>(this Result<{type_string(n)}> Result, Func<{comma_string(n)}, Task<Result<TRes>>> Func)
{{
    if (Result.Failure)
        return Result.To<TRes>();

    var val = await Func({tuple_args(n, "Result.Value")});
    return Infrastructure.Result.Combine(Result, val).To(val.Value);
}}

public static async Task<Result> OnSuccess<{comma_string(n)}>(this Result<{type_string(n)}> Result, Func<{comma_string(n)}, Task<Result>> Func)
{{
    if (Result.Failure)
        return Result;

    var val = await Func({tuple_args(n, "Result.Value")});
    return Infrastructure.Result.Combine(Result, val);
}}

public static async Task<Result<{type_string(n)}>> TeeAsync<{comma_string(n)}>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, Task> f)
{{
    if (x.Success)
        await f({tuple_args(n, "x.Value")});
    return x;
}}

public static async Task<Result<TSuccess>> TransformAsync<{comma_string(n)}, TSuccess>(this Result<{type_string(n)}> x, Func<{comma_string(n)}, Task<TSuccess>> transform)
{{
    if(x.Failure)
        return x.To<TSuccess>();
    return await new Try().Expect().ExecuteAsync(async () => Result.Ok(await transform({tuple_args(n, "x.Value")})));
}}
'''


def make_extensions(n):
    return ''.join(extension_template(i+1) for i in range(n))


def make_existing_extensions(n):
    return ''.join(existing_extension_template(i+1) for i in range(1, n))


def tab(s):
    return '\n'.join('\t' + a for a in s.split('\n'))


num = 8
namespace = f'''using System;
using System.Threading.Tasks;

namespace Sandman.Infrastructure
{{
{tab(make_classes(num))}
    public static class TupleResultExtensions
    {{
{tab(tab(make_extensions(num)))}
{tab(tab(make_existing_extensions(num)))}
    }}
}}
'''

with open('TupleResult.cs', 'w') as f:
    f.write(namespace)