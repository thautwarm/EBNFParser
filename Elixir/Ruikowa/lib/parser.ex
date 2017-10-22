defmodule Parser do
  @moduledoc false

  defmodule Literal do

    def match([word|words], %{__struct__: Regex}=literalParser) do
      case Regex.run(literalParser, word)
      do
        [^word] -> {word, words}
        _       -> {:unmatched, [word|words]}
      end
    end

    def match([word|words], literalParser) when is_bitstring(literalParser) do
      case word do
        ^literalParser -> {word, words}
        _              -> {:unmatched, [word|words]}
      end
    end


  end

  defmodule AstParser do
    defstruct name: nil, strucure: %{:recur=>nil, :starts => [{:isRegex, :beginSign, :cases}]}

    def match([word|words], %{__struct__: AstParser}=astParser) do
      astParser.strucure.starts
        |> Enum.find
            fn
              (true, beginSign, _)->
                case Regex.run(beginSign, word)
                do
                  [^word] -> true
                  _       -> false
                end

              (false, beginSign, _)->
                case beginSign
                do
                  [^word] -> true
                  _       -> false
                end
            end
        |> fn
             (_, _, cases)->
                dosomething
           end
    end

  end



end
