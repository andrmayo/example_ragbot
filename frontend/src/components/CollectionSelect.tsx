interface CollectionSelectProps {
  collections: string[];
  selected: string;
  onSelect: (collection: string) => void;
}

export function CollectionSelect({
  collections,
  selected,
  onSelect,
}: CollectionSelectProps) {
  return (
    <select
      value={selected}
      onChange={(e) => onSelect(e.target.value)}
      className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      {collections.map((collection) => (
        <option key={collection} value={collection}>
          {collection}
        </option>
      ))}
    </select>
  );
}
