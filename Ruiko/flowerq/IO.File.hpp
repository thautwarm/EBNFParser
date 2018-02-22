
/*
TODO: cahcing
*/
struct Writer
{
public:
    ofstream stream;
    void write(const Char *buf)
    {
        stream << buf;
    }
    void close()
    {
        stream.close();
    }
    Writer(const char *filename)
        : stream(filename){};
};

struct Reader
{
public:
    ifstream stream;

    StringBuff read(const Char split)
    {
        StringBuff s;
        Char c;
        while (stream.get(c) && (c != split) && !stream.eof())
        {
            s.push_back(c);
        }
        return s;
    }

    StringBuff read()
    {
        StringBuff s;
        Char c;
        while (stream.get(c) && !stream.eof())
        {
            s.push_back(c);
        }
        return s;
    }
    void close()
    {
        stream.close();
    }
    Reader(const char *filename)
        : stream(filename)
    {
    }
};
template <typename R>
R open(const char *filename)
{
}

template <>
Writer open<Writer>(const char *filename)
{
    return Writer(filename);
}

template <>
Reader open<Reader>(const char *filename)
{
    return Reader(filename);
}
