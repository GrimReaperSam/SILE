function prefix = getprefix(id)

prefix = num2str(id);
if id > 9
    prefix = prefix(end-1:end);
else
    prefix = ['0' prefix(end)];
end
